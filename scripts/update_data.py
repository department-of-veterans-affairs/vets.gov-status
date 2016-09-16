"""Pulls in data to update dashboards"""

import datetime
import json

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

import httplib2

import numpy as np
import pandas as pd


SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
DISCOVERY_URI = ('https://analyticsreporting.googleapis.com/$discovery/rest')
KEY_FILE_LOCATION = 'serviceaccount.p12'
SERVICE_ACCOUNT_EMAIL = 'analytics@inductive-voice-142915.iam.gserviceaccount.com'


def initialize_analyticsreporting():
    """Initializes an analyticsreporting service object.

    Returns:
    analytics an authorized analyticsreporting service object.
    """

    credentials = ServiceAccountCredentials.from_p12_keyfile(
        SERVICE_ACCOUNT_EMAIL, KEY_FILE_LOCATION, scopes=SCOPES)

    http = credentials.authorize(httplib2.Http())

    # Build the service object.
    analytics = build('analytics', 'v4', http=http,
                      discoveryServiceUrl=DISCOVERY_URI)

    return analytics


def get_reports(analytics, view_id):
    """Use the Analytics Service Object to query Analytics Reporting API."""
    return analytics.reports().batchGet(
        body={
            'reportRequests': [{
                    'viewId': view_id,
                    'dateRanges': [{'startDate': '120daysAgo',
                                    'endDate': 'yesterday'}],
                    'metrics': [{'expression': 'ga:users'},
                                {'expression': 'ga:newUsers'}],
                    'dimensions': [{'name': 'ga:isoYearIsoWeek'}]
                },
                {
                    'viewId': view_id,
                    'dateRanges': [{'startDate': '120daysAgo',
                                    'endDate': 'yesterday'}],
                    'metrics': [{'expression': 'ga:users'}],
                    'dimensions': [{'name': 'ga:isoYearIsoWeek'},
                                   {'name': 'ga:deviceCategory'}]
                }]
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
    df['returning'] = df['all'] - df['new']

    users = df.copy()
    del users['new'], users['returning']
    filename = "{}_users.csv".format(board)
    users.to_csv(filename, date_format="%m/%d/%y")

    del df['all']
    filename = "{}_new.csv".format(board)
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

    filename = "{}_mobile.csv".format(board)
    df.to_csv(filename, date_format="%m/%d/%y")


def run_reports(analytics, board, view_id):
    response = get_reports(analytics, view_id)
    user_df = make_df(response['reports'][0])
    output_users(user_df, board)
    device_df = make_df(response['reports'][1])
    output_device(device_df, board)

def main():
    analytics = initialize_analyticsreporting()

    with open('config.json') as json_data_file:
        boards = json.load(json_data_file)

    for board in boards:
        run_reports(analytics, board, boards[board])


if __name__ == '__main__':
    main()
