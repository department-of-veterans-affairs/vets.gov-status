"""Pulls in data to update dashboards"""

import datetime
import json
import os

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

import httplib2

import numpy as np
import pandas as pd
import ruamel.yaml as yaml


SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
DISCOVERY_URI = ('https://analyticsreporting.googleapis.com/$discovery/rest')
KEY_FILE_LOCATION = os.environ['GA_SERVICEACCOUNT']


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


def get_count_report(analytics, view_id, event_name):
    """Use the Analytics Service Object to query Analytics Reporting API.
    """

    # Start on 1 September 2017 which is the cutover date to the unified view
    # Adjustment in the config is the sums from 30 June 2016 (launch of HCA) until
    # 31 August 2017 when the cutover happened.
    startDate = datetime.date(2017,9,1).isoformat()
    # Yesterday
    endDate = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()

    return analytics.reports().batchGet(
        body={
            'reportRequests': [
                {
                    'viewId': view_id,
                    'dateRanges': [{'startDate': startDate,
                                    'endDate': endDate}],
                    'metrics': [{'expression': 'ga:totalEvents'}],
                    'dimensions': [{'name': 'ga:eventLabel'}],
                    "dimensionFilterClauses": [{
                        "filters": [
                            {
                              "dimensionName": "ga:eventLabel",
                              "operator": "EXACT",
                              "expressions": event_name
                            }
                            ]}],
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

    return raw_df



def run_report(analytics, count, details):
    response = get_count_report(analytics, details['view'], details['event_name'])
    df = make_df(response['reports'][0])
    return df.at[0,'ga:totalEvents'] + details['adjustment']

def main():
    analytics = initialize_analyticsreporting()

    with open(os.path.join(os.environ['CONFIG_DIR'], 'ga_config.json')) as json_data_file:
        config = json.load(json_data_file)
        counts = config['counts']


    output_file = os.path.join(os.environ['DATA_DIR'],'counts.yml')
    with open(output_file, 'r') as output:
        output_dict = yaml.load(output, yaml.RoundTripLoader)

        for count in counts:
            total = run_report(analytics, count, counts[count])
            output_dict[count] = "{:,}".format(total)

    with open(output_file, 'w') as output:
        yaml.dump(output_dict, output, Dumper=yaml.RoundTripDumper, default_style='"')

if __name__ == '__main__':
    main()
