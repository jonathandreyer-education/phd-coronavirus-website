# -*- coding: utf-8 -*-

import requests
import csv
import pandas as pd


CATEGORIES = ['Confirmed', 'Deaths', 'Recovered']


def process_data(data):
    # Extract data
    _data = list(csv.DictReader(data.splitlines()))
    df = pd.DataFrame(_data)
    df['Country/Region'].replace({'Mainland China': 'China'}, inplace=True)

    # Remove useless columns
    df = df.drop(["Province/State", "Lat", "Long"], axis=1)

    # Convert to numerical values
    cols = [i for i in df.columns if i not in ["Country/Region"]]
    for col in cols:
        df[col] = pd.to_numeric(df[col])

    # Regroup by sum all row of same country
    df = df.groupby(['Country/Region']).agg('sum')

    # Set index as date
    df_T = df.T
    df_T['Date'] = pd.to_datetime(df_T.index)
    df_T.set_index('Date', inplace=True)

    # Transpose data
    df_cleaned = df_T.copy()

    # Find latest date
    ts = df_cleaned.index.max()

    return ts, df_cleaned


def get_data_from_local():
    # Download the dataset (Derivated from remote version)
    BASE_FILES = './time_series/time_series_2019-ncov-{}.csv'
    DATAFRAMES = {'timestamp': None}

    # Iterate through all files
    for _category in CATEGORIES:
        pathfile = BASE_FILES.format(_category)
        with open(pathfile) as file:
            # Read data from file
            _text = file.read()

            # Process data
            ts, df = process_data(_text)

            # Store data processed
            DATAFRAMES[_category.lower()] = df
            DATAFRAMES['timestamp'] = ts

            if DATAFRAMES['timestamp'] is None:
                DATAFRAMES['timestamp'] = ts
            else:
                if DATAFRAMES['timestamp'] != ts:
                    print('Warning, the latest value is not equal than other feed!')
                else:
                    DATAFRAMES['timestamp'] = ts

    return DATAFRAMES


def get_data_from_http():
    # Download the dataset (Source: https://github.com/nat236919/Covid2019API/blob/master/app/helper.py)
    BASE_URL = 'https://raw.githubusercontent.com/CSSEGISandData/2019-nCoV/master/time_series/time_series_2019-ncov-{}.csv'
    DATAFRAMES = {'timestamp': None}

    # Iterate through all files
    for _category in CATEGORIES:
        # Read data from URL
        url = BASE_URL.format(_category)
        res = requests.get(url)
        _text = res.text

        # Process data
        ts, df = process_data(_text)

        # Store data processed
        DATAFRAMES[_category.lower()] = df
        DATAFRAMES['timestamp'] = ts

        if DATAFRAMES['timestamp'] is None:
            DATAFRAMES['timestamp'] = ts
        else:
            if DATAFRAMES['timestamp'] != ts:
                print('Warning, the latest value is not equal than other feed!')
            else:
                DATAFRAMES['timestamp'] = ts

    return DATAFRAMES


def get_data(use_local=False):
    if use_local:
        return get_data_from_local()
    else:
        return get_data_from_http()


class DataModel:
    def __init__(self):
        self._data = None
        self._statical_data = {'SARS':{'deaths': 774, 'confirmed': 8_098, 'recovered': 7_324},
                               'MERS':{'deaths': 862, 'confirmed':2_506, 'recovered':1_644}}
        self.pull_data()

    def pull_data(self):
        try:
            self._data = get_data(use_local=False)
            print('Data fetched')
        except:
            print('Error to get data')

    def get_latest_value(self):
        _d = {}

        for _category in CATEGORIES:
            _df = self._data[_category.lower()]
            _value = sum([int(v) for v in _df.loc[_df.index.max()]])
            _d[_category.lower()] = _value

        time = self._data['timestamp'].strftime("%d/%m/%Y %H:%M:%S")

        return {'timestamp': time, 'data': _d}

    def get_timeseries(self):
        _data = {}

        # Sum for every timestamp
        for _category in CATEGORIES:
            _d = []
            _df = self._data[_category.lower()]
            _df = _df.sort_index()

            for l in _df.iterrows():
                _v = {}
                _v['timestamp'] = l[0].strftime("%d/%m/%Y %H:%M:%S")
                _v['value'] = sum([int(i) for i in l[1]])
                _d.append(_v)

            _data[_category.lower()] = _d

        return _data

    def get_static(self):
        return self._statical_data
