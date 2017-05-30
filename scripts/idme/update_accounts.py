import datetime
import os

from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

import httplib2

import pandas as pd
import ruamel.yaml as yaml

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
DISCOVERY_URI = ('https://analyticsreporting.googleapis.com/$discovery/rest')
KEY_FILE_LOCATION = os.environ['GA_SERVICEACCOUNT']
SERVICE_ACCOUNT_EMAIL = 'analytics@inductive-voice-142915.iam.gserviceaccount.com'

def fetch_sheet_data():
    """Initializes an analyticsreporting service object.

    Returns:
    analytics an authorized analyticsreporting service object.
    """

    credentials = ServiceAccountCredentials.from_p12_keyfile(
        SERVICE_ACCOUNT_EMAIL, KEY_FILE_LOCATION, scopes=SCOPES)

    http = credentials.authorize(httplib2.Http())

    # Build the service object.
    service =  discovery.build('sheets', 'v4', credentials=credentials)

    request = (service.spreadsheets().values().get(
                spreadsheetId='1WYHGRN51c7b1yVceA8uEG16lIhikxwOe25wbCSjB-S4',
                range='A1:C',
                valueRenderOption='FORMATTED_VALUE',
                dateTimeRenderOption='FORMATTED_STRING'))
    return request.execute()


def make_df(values):
    values_df = pd.DataFrame(values[1:], columns=values[0])

    values_df = values_df[values_df['loa1signups'].notnull()]

    values_df['day'] = pd.to_datetime(values_df['day'])
    values_df = values_df.set_index('day')

    values_df[['loa1signups','loa3signups']] = values_df[['loa1signups','loa3signups']].astype('int')

    return values_df


def output_loa3_count(loa3_accounts):

    output_file = os.path.join(os.environ['DATA_DIR'],'counts.yml')
    with open(output_file, 'r') as output:
        output_dict = yaml.load(output, yaml.RoundTripLoader)

    output_dict['loa3accounts'] = "{:,}".format(loa3_accounts)

    with open(output_file, 'w') as output:
        yaml.dump(output_dict, output, Dumper=yaml.RoundTripDumper, default_style='"')

def find_sunday():
    """Finds the prior Sunday to ensure a full week of data

    returns a datetime representing that Sunday"""

    today = datetime.date.today()

    # Monday is 1 and Sunday is 7 for isoweekday()
    days_after_sunday = datetime.timedelta(days=today.isoweekday())
    return today - days_after_sunday

def make_daily_chart(df):

    df = filter_timerange(df)
    df = df.reset_index()

    # Find the iso week of every day
    df['week']= df['day'].apply(lambda x: x.date().isocalendar()[1])

    # Create mapping from days to weeks. We'll lose this when
    # we sum because dates don't sum
    week_to_day = df[['day','week']].groupby('week').agg('max')

    df = df.groupby('week').agg('sum')
    df = df.reset_index()

    # Add back in the last day of that week
    df['day'] = df['week'].apply(lambda x: week_to_day.loc[x,'day'])

    output_csv(df, "core_signups_weekly.csv")

def make_total_chart(df):

    df = filter_timerange(df)
    df = df.reset_index()

    # Find the iso week of every day
    df['week']= df['day'].apply(lambda x: x.date().isocalendar()[1])

    df = df.groupby('week').max()

    output_csv(df, "core_signupstotal_weekly.csv")

def output_csv(df, csv):
    df = df.set_index('day')
    if 'week' in df:
        del df['week']
    df.to_csv(os.path.join(os.environ['DATA_DIR'],csv),
              date_format="%m/%d/%y")

def filter_timerange(df):
    sunday = find_sunday()
    endDate = pd.Timestamp(find_sunday())
    startDate = pd.Timestamp(sunday - datetime.timedelta(days=139))
    return df[startDate:endDate]


def main():

    response = fetch_sheet_data()
    values = response['values']
    daily_signups_df = make_df(values)

    # The added values are the totals prior to 1/6/2017 when the online gsheet counts begin
    totals = daily_signups_df.sum() + pd.Series({'loa1signups': 26701,
                                                 'loa3signups': 11046})
    output_loa3_count(totals['loa3signups'])

    make_daily_chart(daily_signups_df)

    total_signups_df = daily_signups_df.cumsum() + pd.Series({'loa1signups': 26701, 'loa3signups': 11046})
    make_total_chart(total_signups_df)

if __name__ == '__main__':
    main()
