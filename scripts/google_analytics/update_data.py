"""Pulls in data to update dashboards"""

import datetime
import json
import os

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

import httplib2

import numpy as np
import pandas as pd


SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
DISCOVERY_URI = ('https://analyticsreporting.googleapis.com/$discovery/rest')
KEY_FILE_LOCATION = os.environ['GA_SERVICEACCOUNT']
SERVICE_ACCOUNT_EMAIL = 'analytics@inductive-voice-142915.iam.gserviceaccount.com'


def initialize_analyticsreporting():
    """Initializes an analyticsreporting service object.

    Returns:
    analytics an authorized analyticsreporting service object.
    """

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
      KEY_FILE_LOCATION, SCOPES)

    # Build the service object.
    analytics = build('analyticsreporting', 'v4', credentials=credentials)

    return analytics


def find_sunday():
    """Finds the prior Sunday to ensure a full week of data

    returns a datetime representing that Sunday"""

    today = datetime.date.today()

    # Monday is 1 and Sunday is 7 for isoweekday()
    days_after_sunday = datetime.timedelta(days=today.isoweekday())
    return today - days_after_sunday


def get_reports(analytics, view_id, page_filter):
    """Use the Analytics Service Object to query Analytics Reporting API.

    Pulls data from the prior full Sunday to 20 full weeks prior
    """
    startDate = (find_sunday() - datetime.timedelta(days=139)).isoformat()
    endDate = find_sunday().isoformat()

    return analytics.reports().batchGet(
        body={
            'reportRequests': [
                {
                    'viewId': view_id,
                    'dateRanges': [{'startDate': startDate,
                                    'endDate': endDate}],
                    'metrics': [{'expression': 'ga:users'},
                                {'expression': 'ga:newUsers'}],
                    'dimensions': [{'name': 'ga:isoYearIsoWeek'}],
                    "dimensionFilterClauses": [{
                        "filters": [
                            {
                              "dimensionName": "ga:pagePath",
                              "operator": "REGEXP",
                              "expressions": page_filter
                            }
                            ]}],
                },
                {
                    'viewId': view_id,
                    'dateRanges': [{'startDate': startDate,
                                    'endDate': endDate}],
                    'metrics': [{'expression': 'ga:sessions'}],
                    'dimensions': [{'name': 'ga:isoYearIsoWeek'},
                                   {'name': 'ga:deviceCategory'}],
                    "dimensionFilterClauses": [{
                       "filters": [
                           {
                             "dimensionName": "ga:pagePath",
                             "operator": "REGEXP",
                             "expressions": page_filter
                           }
                           ]}],
                },
                {
                    'viewId': view_id,
                    'dateRanges': [{'startDate': startDate,
                                    'endDate': endDate}],
                    'metrics': [{'expression': 'ga:pageviews'}],
                    'dimensions': [{'name': 'ga:isoYearIsoWeek'}],
                    "dimensionFilterClauses": [{
                       "filters": [
                           {
                             "dimensionName": "ga:pagePath",
                             "operator": "REGEXP",
                             "expressions": page_filter
                           }
                           ]}],
                }
            ],
            "useResourceQuotas": True
        }
    ).execute()

def get_click_reports(analytics, view_id):
    """Use the Analytics Service Object to query Analytics Reporting API.

    Pulls data from the prior full Sunday to 20 full weeks prior
    """
    startDate = (find_sunday() - datetime.timedelta(days=139)).isoformat()
    endDate = find_sunday().isoformat()

    return analytics.reports().batchGet(
        body={
            'reportRequests': [{
                    'viewId': view_id,
                    'dateRanges': [{'startDate': startDate,
                                    'endDate': endDate}],
                    'metrics': [{'expression': 'ga:totalEvents'}],
                    'dimensions': [{'name': 'ga:isoYearIsoWeek'}],
                    "dimensionFilterClauses": [{
                        "operator": "OR",
                        "filters": [
                            {
                              "dimensionName": "ga:eventLabel",
                              "operator": "PARTIAL",
                              "expressions": "veteranscrisisline"
                            },
                            {
                              "dimensionName": "ga:eventLabel",
                              "operator": "PARTIAL",
                              "expressions": "sms:838255"
                            },
                            {
                              "dimensionName": "ga:eventLabel",
                              "operator": "PARTIAL",
                              "expressions": "tel:18002738255"
                            },
                            {
                              "dimensionName": "ga:eventAction",
                              "operator": "PARTIAL",
                              "expressions": "veteranscrisisline"
                            },
                            {
                              "dimensionName": "ga:eventAction",
                              "operator": "PARTIAL",
                              "expressions": "sms:838255"
                            },
                            {
                              "dimensionName": "ga:eventAction",
                              "operator": "PARTIAL",
                              "expressions": "tel:18002738255"
                            },
                            ]}],
                    "includeEmptyRows": "true",
                }
            ],
            "useResourceQuotas": True
        }
    ).execute()

def make_df(report):
    """Turn a single report from a Google Analytics response into dataframe"""

    dimLabels = report['columnHeader']['dimensions']
    metricLabels = [entry['name']
                    for entry
                    in report['columnHeader']['metricHeader']['metricHeaderEntries']]

    output = []
    for row in report['data']['rows']:
        current_data = {}

        for k, v in zip(dimLabels, row['dimensions']):
            current_data[k] = v

        metricValues = [d['values'] for d in row['metrics']]
        metricValues = [item for sublist in metricValues for item in sublist]
        for k, v in zip(metricLabels, metricValues):
            current_data[k] = int(v)

        output.append(current_data)

    raw_df = pd.DataFrame(output)

    # Set the day equal to the Sunday that ends that week
    raw_df['day'] = raw_df['ga:isoYearIsoWeek'].apply(
                    lambda d: datetime.datetime.strptime(d + '-0', "%Y%W-%w"))
    raw_df['day'] = pd.to_datetime(raw_df['day'])
    raw_df = raw_df.set_index('day')
    del raw_df['ga:isoYearIsoWeek']

    return raw_df


def output_users(df, board):
    """Output a csv from dataframe contents."""

    df.columns = ['new', 'all']
    del df['new']
    filename = os.path.join(os.environ['DATA_DIR'],
                            "{}_users.csv".format(board))
    df.to_csv(filename, date_format="%m/%d/%y")

def output_device(df, board):

    df = df.reset_index()

    mobile = df[df['ga:deviceCategory'] != 'desktop'].groupby('day').agg(np.sum)
    mobile.columns = ['mobile']
    #print(mobile)

    df = df[df['ga:deviceCategory'] == 'desktop'].groupby('day').agg(np.sum)
    df.columns = ['desktop']
    #print(desktop)

    df['mobile'] = mobile['mobile']
    df['all'] = df['desktop'] + df['mobile']
    df['mobile'] = (df['mobile'] / df['all']) * 100
    df['desktop'] = (df['desktop'] / df['all']) * 100

    filename = os.path.join(os.environ['DATA_DIR'],
                            "{}_mobile.csv".format(board))
    df.to_csv(filename, date_format="%m/%d/%y")

def output_pageviews(df, board):
    """Output a csv from dataframe contents."""

    df.columns = ['views']
    filename = os.path.join(os.environ['DATA_DIR'],
                            "{}_views.csv".format(board))
    df.to_csv(filename, date_format="%m/%d/%y")



def run_reports(analytics, board, view_id, page_filter=""):
    response = get_reports(analytics, view_id, page_filter)
    user_df = make_df(response['reports'][0])
    output_users(user_df, board)
    device_df = make_df(response['reports'][1])
    output_device(device_df, board)
    pageviews_df = make_df(response['reports'][2])
    output_pageviews(pageviews_df, board)

def run_click_reports(analytics, board, view_id):
    response = get_click_reports(analytics, view_id)
    vcl_df = make_df(response['reports'][0])
    output_clicks(vcl_df, board)

def output_clicks(df, board):
    """Output a csv from dataframe contents."""

    df.columns = ["all"]
    filename = os.path.join(os.environ['DATA_DIR'],
                            "{}_clicks.csv".format(board))
    df.to_csv(filename, date_format="%m/%d/%y")

def main():
    analytics = initialize_analyticsreporting()

    with open(os.path.join(os.environ['CONFIG_DIR'], 'ga_config.json')) as json_data_file:
        config = json.load(json_data_file)
        boards = config['charts']
        clicks = config['clicks']

    for board in boards:
        details = boards[board]
        run_reports(analytics, board, details['view'], details['page_filter'])

    for click in clicks:
        details = clicks[click]
        run_click_reports(analytics, click, details['view'])


if __name__ == '__main__':
    main()
