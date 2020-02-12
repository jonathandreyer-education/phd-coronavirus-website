# -*- coding: utf-8 -*-

import requests
import csv
import pandas as pd


def get_data_from_local():
    # Download the dataset (Derivated from remote version)
    BASE_FILES = './time_series/time_series_2019-ncov-{}.csv'
    CATEGORIES = ['Confirmed', 'Deaths', 'Recovered']
    DATAFRAMES = {}

    # Iterate through all files
    for _category in CATEGORIES:
        pathfile = BASE_FILES.format(_category)
        with open(pathfile) as file:
            _text = file.read()

            # Extract data
            data = list(csv.DictReader(_text.splitlines()))
            df = pd.DataFrame(data)

            # Data Cleaning
            df = df.iloc[:, [1, -1]]  # Select only Country and its last values
            df.columns = ['Country/Region', _category]
            pd.to_numeric(df[_category])
            df['Country/Region'].replace({'Mainland China': 'China'}, inplace=True)
            df.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)

            DATAFRAMES[_category.lower()] = df

            DATAFRAMES['timestamp'] = _text.splitlines()[0].split(',')[-1]

    return DATAFRAMES


def get_data_from_http():
    # Download the dataset (Source: https://github.com/nat236919/Covid2019API/blob/master/app/helper.py)
    BASE_URL = 'https://raw.githubusercontent.com/CSSEGISandData/2019-nCoV/master/time_series/time_series_2019-ncov-{}.csv'
    CATEGORIES = ['Confirmed', 'Deaths', 'Recovered']
    DATAFRAMES = {}

    # Iterate through all files
    for category in CATEGORIES:
        url = BASE_URL.format(category)
        res = requests.get(url)
        text = res.text

        # Extract data
        data = list(csv.DictReader(text.splitlines()))
        df = pd.DataFrame(data)

        # Data Cleaning
        df = df.iloc[:, [1, -1]]  # Select only Country and its last values
        df.columns = ['Country/Region', category]
        pd.to_numeric(df[category])
        df['Country/Region'].replace({'Mainland China': 'China'}, inplace=True)
        df.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)

        DATAFRAMES[category.lower()] = df

        DATAFRAMES['timestamp'] = text.splitlines()[0].split(',')[-1]

    return DATAFRAMES


def get_data(use_local=False):
    if use_local:
        return get_data_from_local()
    else:
        return get_data_from_http()


class DataModel:
    def __init__(self):
        self._data = None
        self.pull_data()

    def pull_data(self):
        try:
            self._data = get_data(use_local=False)
            print('Data fetched')
        except:
            print('Error to get data')

    def get_latest_value(self):
        deaths = sum([int(i) for i in self._data['deaths']['Deaths']])
        confirmed = sum([int(i) for i in self._data['confirmed']['Confirmed']])
        recovered = sum([int(i) for i in self._data['recovered']['Recovered']])
        latest_data = {'deaths': deaths, 'confirmed': confirmed, 'recovered': recovered}

        time = self._data['timestamp']

        return {'timestamp': time, 'data': latest_data}

    def get_case_by_country(self):
        pass
