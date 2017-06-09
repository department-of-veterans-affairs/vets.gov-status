import datetime
import json
import os

import pandas as pd
import requests
import ruamel.yaml as yaml

PROXY_CONFIG    = {
  'http': 'socks5h://172.17.0.1:2001',
  'https': 'socks5h://172.17.0.1:2001'
}

def find_last_sunday():
  """Finds the prior Sunday to ensure a full week of data

  returns a datetime representing that Sunday"""

  today = datetime.date.today()

  # Monday is 1 and Sunday is 7 for isoweekday()
  days_after_sunday = datetime.timedelta(days=today.isoweekday())
  return today - days_after_sunday

def df_from_response(response):
  """Create a pandas dataframe from a prometheus API response object

  Parameters:
  `response` -- a response object from a "requests" request

  Example:
    query:
      sum(rate(nginx_http_request_total{status=~"5.."}[5m]))
        / sum(rate(nginx_http_request_total[5m]))
    returns:
      | ts         | day                       | value |
      | ---        | ---                       | --- |
      | 1492445066 | 2017-04-17 10:04:26 -0600 | 0   |
      | 1492531466 | 2017-04-18 10:04:26 -0600 | 0   |
      | 1492617866 | 2017-04-19 10:04:26 -0600 | 0   |


  Returns: a pandas DataFrame object
  """

  data = {}

  # print(response.text)

  parsed_response = response.json()

  # Collect timestamps from each metric. Confirm that all metrics have consistent
  # tiemstamps, or raise a ValueError. Supports 'vector' and 'matrix' response types
  for ts in parsed_response['data']['result']:
    if parsed_response['data']['resultType'] == 'vector':
      timestamps = [ts['value'][0]]
    elif parsed_response['data']['resultType'] == 'matrix':
      timestamps = [v[0] for v in ts['values']]
    else:
      raise ValueError('Unsupported prometheus response type')

    if data.get('timestamp', None) is None:
      data['timestamp'] = timestamps
    elif data['timestamp'] != timestamps:
      # When group is supported:
      raise ValueError('Inconsistent TS timestamps not supported')


  # Collect the data from each metric.
  for ts in parsed_response['data']['result']:
    if parsed_response['data']['resultType'] == 'vector':
      data['value'] = [ts['value'][1]]
    elif parsed_response['data']['resultType'] == 'matrix':
      data['value'] = [v[1] for v in ts['values']]

  # Convert the data into a data frame and parse the timestamps into something usable
  df = pd.DataFrame.from_dict(data)
  df['day'] = df['timestamp'].apply(lambda ts: datetime.datetime.fromtimestamp(ts))
  return df


def query_prometheus(query):
  """Query the configured prometheus endpoint

  Parameters:
  `query` -- a prometheus query definition

  Example:
  `query`:
    `endpoint` -- the envvar with an API endpoint to hit
    `endpoint_path` -- the path on API. Either /query_range or /query
    `params`:
      `query`: A query, e.g., 'avg_over_time(script_success[24h])'
      `days_back` -- How many days prior to last sunday to query
      `step` -- Result resolution

  Returns: a response object from Prometheus
  """

  qparams = query['params'].copy()

  if 'days_back' in qparams:
      end = find_last_sunday()
      start = end - datetime.timedelta(days=qparams['days_back'])
      del qparams['days_back']
      qparams['start'] = pd.Timestamp(start).isoformat() + 'Z'
      qparams['end']= pd.Timestamp(end).isoformat() + 'Z'

  print(query['endpoint']+query['endpoint_path'])
  return requests.get(query['endpoint']+query['endpoint_path'],
                      params=qparams,
                      proxies=PROXY_CONFIG)

def write_report(report_definition):
    """ Write a CSV with 2 weeks of TS data for the given prometheus query

    Parameters:
    `report_definition` -- a dictionary defining a query, source, and destination path

    `report_definition`:
      `query`:
        `endpoint` -- the envvar with an API endpoint to hit
        `endpoint_path` -- the path on API. Either /query_range or /query
        `params`:
          `query` -- A prometheus query
          `days_back` -- How many days prior to last sunday to query
          `step` -- Result resolution

      `path` -- path to write CSV output

    Returns:
    Nothing of value
    """

    response = query_prometheus(report_definition['query'])
    df = df_from_response(response)
    df.to_csv(report_definition['path'], date_format='%m/%d/%y')

def make_cloud_data():
    output = {}

    df = pd.read_csv("error_rate.csv", usecols=['day','value'], index_col='day', parse_dates=True)
    output['error_rate'] = '{:.4%}'.format(df[-7:].mean().value.item())

    df = pd.read_csv("reachability.csv", usecols=['day','value'], index_col='day', parse_dates=True)
    output['reachability'] = '{:.4%}'.format(df[-7:].mean().value.item())

    df = pd.read_csv("deployments_monthly.csv", usecols=['day','value'], index_col='day', parse_dates=True)
    output['deployments'] = df.iloc[0,0].item()

    output_file = os.path.join(os.environ['DATA_DIR'],'cloud.yml')
    with open(output_file, 'w') as outfile:
        outfile.write(yaml.dump(output, default_flow_style=False))

def main():

    with open(os.path.join(os.environ['CONFIG_DIR'], 'prometheus_config.json')) as json_data_file:
        config = json.load(json_data_file)

    for report_definition in config['reports']:
        write_report(report_definition)

    make_cloud_data()

if __name__ == '__main__':
    main()
