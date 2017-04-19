"""Pulls in data to update dashboards"""

import datetime
import os

import numpy as np
import pandas as pd

def find_sunday():
    """Finds the prior Sunday to ensure a full week of data

    returns a datetime representing that Sunday"""

    today = datetime.date.today()

    # Monday is 1 and Sunday is 7 for isoweekday()
    days_after_sunday = datetime.timedelta(days=today.isoweekday())
    return today - days_after_sunday

def run_report(csv):
    df = get_df(csv)

    week_to_day = df.reset_index()
    week_to_day = week_to_day[['day','week']].groupby('week').agg('max')

    weekly_df = df.groupby('week').agg('sum')
    weekly_df = weekly_df.reset_index()
    weekly_df['day'] = weekly_df['week'].apply(lambda x: week_to_day.loc[x,'day'])
    weekly_df = weekly_df.set_index('day')
    del weekly_df['week']

    filename = os.path.splitext(os.path.basename(csv))[0] + "_weekly.csv"
    weekly_df.to_csv(filename, date_format="%m/%d/%y")

def get_df(csv):
    df = pd.read_csv(csv, index_col="day", parse_dates=True)
    df = filter_timerange(df)
    df['week']= df.index
    df['week']= df['week'].apply(lambda x: x.date().isocalendar()[1])
    return df

def filter_timerange(df):
    sunday = find_sunday()
    endDate = pd.Timestamp(find_sunday())
    startDate = pd.Timestamp(sunday - datetime.timedelta(days=139))
    return df[startDate:endDate]

def main():

    csvs = ["../_data/core_signups.csv"]

    for csv in csvs:
        run_report(csv)


if __name__ == '__main__':
    main()
