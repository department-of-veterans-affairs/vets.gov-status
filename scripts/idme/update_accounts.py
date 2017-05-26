from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

import httplib2

import pandas as pd
import ruamel.yaml as yaml

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
DISCOVERY_URI = ('https://analyticsreporting.googleapis.com/$discovery/rest')
#TODO: Update this to envvar
KEY_FILE_LOCATION = 'serviceaccount.p12'
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

    output_dict['loa3accounts'] = loa3_accounts

    with open(output_file, 'w') as output:
        yaml.dump(output_dict, output, Dumper=yaml.RoundTripDumper, default_style='"')


def main():

    reponse = fetch_sheet_data()
    values = response['values']
    daily_signups_df = make_df(values)

    # The added values are the totals prior to 1/6/2017 when the online gsheet counts begin
    totals = daily_signups_df.sum() + pd.Series({'loa1signups': 26701, 'loa3signups': 11046})
    output_loa3_count(totals['loa3signups'])

    total_signups_df = values_df.cumsum() + pd.Series({'loa1signups': 26701, 'loa3signups': 11046})

if __name__ == '__main__':
    main()
