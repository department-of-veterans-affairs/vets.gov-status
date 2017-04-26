import code
import datetime
import os
import pandas as pd
import requests

PROXY_CONFIG    = {
  'http': 'socks5://127.0.0.1:2001'
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
    `endpoint`: 'http://prometheus-def.vetsgov-internal/api/v1/query',
    `params`:
      `query`: 'avg_over_time(script_success[24h])'

  Returns: a response object from Prometheus
  """

  qparams = query['params'].copy()

  # Convert start and end to unix timestamps
  for k in ['start', 'end']:
    p = qparams.get(k, None)
    if p and type(p) in (datetime.datetime, datetime.date):
      qparams[k] = (p - datetime.date(1970, 1, 1)).total_seconds()

  return requests.get(query['endpoint'], params=qparams, proxies=PROXY_CONFIG)

def write_report(report_definition):
    """ Write a CSV with 2 weeks of TS data for the given prometheus query

    Parameters:
    `report_definition` -- a dictionary defining a query, source, and destination path

    `report_definition`:
      `query`:
        `endpoint` -- the API endpoint to hit. This can be either SOURCE + /query or SOURCE + /query_range
        `params`:
          `query` -- A prometheus query
          `start` -- DateTime object, use with ranged queries only, starting time
          `end` -- DateTime object, use with ranged queries only, ending time
          `step` -- Result resolution

      `path` -- path to write CSV output

    Returns:
    Nothing of value
    """

    response = query_prometheus(report_definition['query'])
    df = df_from_response(response)
    df.to_csv(report_definition['path'], date_format='%m/%d/%y')

REPORTS = [
  # Estimated daily deployments
  {
    'query': {
      'endpoint': os.environ['PROMETHEUS_API_UTILITY'] + '/query_range',
      'params': {
        'query': 'round(sum(changes(default_jenkins_builds_duration_milliseconds_summary_sum{exported_job="deploys/vets-api-prod"}[24h]))) + round(sum(delta(default_jenkins_builds_duration_milliseconds_summary_count{exported_job="testing/vets-website/production"}[24h])))',
        'start': find_last_sunday() - datetime.timedelta(days=14),
        'end': find_last_sunday(),
        'step': '24h',
      },
    },

    'path': '../_data/deployments_daily.csv',
  },

  # Projected monthly deployment count
  {
    'query': {
      'endpoint': os.environ['PROMETHEUS_API_UTILITY'] + '/query',
      'params': {
        'query': 'round(sum(changes(default_jenkins_builds_duration_milliseconds_summary_sum{exported_job="deploys/vets-api-prod"}[2w]))) * 2',
      },
    },

    'path': '../_data/deployments_monthly.csv',
  },

  # Error rate daily
  {
    'query': {
      'endpoint': os.environ['PROMETHEUS_API_SITE'] + '/query_range',
      'params': {
        'query': 'sum(rate(nginx_http_request_total{status=~"5.."}[24h])) / sum(rate(nginx_http_request_total[24h]))',
        'start': find_last_sunday() - datetime.timedelta(days=14),
        'end': find_last_sunday(),
        'step': '24h',
      },
    },

    'path': '../_data/error_rate.csv',
  },

  # Total system reachability average (daily) (single EW instance)
  {
    'query': {
      'endpoint': os.environ['PROMETHEUS_API_SITE'] + '/query_range',
      'params': {
        'query': 'avg(avg_over_time(probe_success{job="site"}[24h]))',
        'start': find_last_sunday() - datetime.timedelta(days=14),
        'end': find_last_sunday(),
        'step': '24h',
      },
    },

    'path': '../_data/reachability.csv',
  },
]


for report_definition in REPORTS:
  write_report(report_definition)
