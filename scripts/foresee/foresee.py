from os import environ, path
from tenacity import retry, stop_after_attempt, wait_exponential, before_sleep_log, retry_if_exception_type
import csv
import requests
import logging
import pandas as pd

from utils.calculation_utils import calculate_trend
from utils.datetime_utils import find_last_twelve_months, find_last_thirty_days, one_year_before
from foresee.foresee_helpers import make_table_from_foresee_response, get_average_score

MEASURE_ID = "8847572"

AUTHORIZATION = 'authorization'

CSAT_SCORE = 'csat_score'
MONTH_DATA = 'month_data'
DATE_COLUMN = 'date'


def authenticate():
    url = "https://api.foresee.com/v1/token"

    querystring = {"scope": "r_cx_basic", "grant_type": "client_credentials"}

    headers = {
        'accept': "application/json",
        'content-type': "application/json",
        'authorization': "Basic " + environ.get('FORESEE_CREDENTIALS')
    }

    response = requests.request("POST", url, headers=headers, params=querystring)

    if response.status_code != 200:
        raise PermissionError

    return response.json()['access_token']


def get_measure_data(bearer_token, from_date, to_date):
    offset = 0
    url = "https://api.foresee.com/v1/measures/" + MEASURE_ID + "/data"
    headers = {
        'accept': 'application/json',
        AUTHORIZATION: "Bearer " + bearer_token
    }
    querystring = {
        "from": from_date,
        "to": to_date,
        "excludeResponseDetails": "false",
        "excludeMQ": "true",
        "excludeCQ": "true",
        "excludePassedParams": "false",
        "excludeLatentScores": "false",
        "offset": str(offset),
        "limit": "100"
    }
    measure_data = []
    has_more = True

    while has_more:
        logging.info("Downloading page: {:n} ".format(offset))
        response = send_one_request(headers, querystring, url)
        response_json = response.json()
        has_more = response_json['hasMore']
        offset += 1
        querystring['offset'] = str(offset)
        measure_data.extend(response_json['items'])

    logging.debug(measure_data)
    return measure_data


def renew_token(retry_state):
    new_token = authenticate()
    retry_state.args[0][AUTHORIZATION] = "Bearer " + new_token


class ForeSeeError(RuntimeError):
    pass


@retry(
    retry=retry_if_exception_type(ForeSeeError),
    wait=wait_exponential(multiplier=3, min=10, max=50),
    stop=stop_after_attempt(5),
    before_sleep=before_sleep_log(logging.getLogger(), logging.WARNING),
    after=renew_token,
    reraise=True
)
def send_one_request(headers, querystring, url):
    response = requests.request("GET", url, headers=headers, params=querystring)
    if response.status_code != 200:
        fail_reason = str(response.status_code) + " " + response.text
        raise ForeSeeError(fail_reason)
    return response


def calculate_average_satisfaction(items):
    extracted_csats = (
        next(latent_score['score']
             for latent_score in item['latentScores'] if latent_score['name'] == 'Satisfaction')
        for item in items
    )
    return round(sum(extracted_csats) / len(items), 1)


def fetch_last_12_months_data():
    last_year_data = []
    last_twelve_months = find_last_twelve_months()

    bearer_token = authenticate()

    # get values for the last 12 months and calculate average for each month
    for start_end_date in last_twelve_months:
        month_data = get_measure_data(bearer_token, start_end_date[0].isoformat(),
                                      start_end_date[1].isoformat())
        month_year_text = str(start_end_date[0].month) + '/' + str(start_end_date[0].year)
        one_month_dict = {
            DATE_COLUMN: month_year_text,
            MONTH_DATA: month_data,
            CSAT_SCORE: calculate_average_satisfaction(month_data)
        }
        last_year_data.append(one_month_dict)
        logging.info("Calculated %s average: %.2f", month_year_text, one_month_dict[CSAT_SCORE])
    return last_year_data


def get_foresee_items_for_services():
    start_date, end_date = find_last_thirty_days()
    recent_items = get_measure_data(authenticate(), start_date, end_date)
    recent_df = pd.DataFrame(make_table_from_foresee_response(recent_items))

    last_year_items = get_measure_data(authenticate(), one_year_before(start_date), one_year_before(end_date))
    last_year_df = pd.DataFrame(make_table_from_foresee_response(last_year_items))

    return recent_df, last_year_df


def fetch_foresee_data_for_services(services):
    recent_df, last_year_df = get_foresee_items_for_services()

    service_data = {}

    for service in services:
        page_path = service['page_path_filter']
        recent_csat_score = round(get_average_score(recent_df, page_path), 1)
        last_year_csat_score = round(get_average_score(last_year_df, page_path), 1)
        service_data[service['title']] = {
            'csat': recent_csat_score,
            'csat_trend': round(calculate_trend(last_year_csat_score, recent_csat_score))
        }

    return service_data


def write_to_csv(twelve_months_scores):
    full_filename = path.join(environ['DATA_DIR'], 'csat_score.csv')
    mode = 'x'
    if path.exists(full_filename):
        mode = 'w'

    with open(full_filename, mode) as csv_file:
        csv_columns = [DATE_COLUMN, CSAT_SCORE]
        writer = csv.DictWriter(csv_file, fieldnames=csv_columns, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(twelve_months_scores)


def update_csat():
    # get dates for last 12 months
    last_year_data = fetch_last_12_months_data()
    write_to_csv(last_year_data)
    return fetch_last_month_csat(last_year_data)


def fetch_last_month_csat(last_year_data):
    return last_year_data[-1][CSAT_SCORE]
