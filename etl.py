import requests
import time
import os
import pandas as pd
from influxdb import DataFrameClient

SERIES = {
    'confirmed': "time_series_19-covid-Confirmed.csv",
    'deaths': "time_series_19-covid-Deaths.csv",
    'recovered': "time_series_19-covid-Recovered.csv",
}

TAG_COLS = ['Province/State', 'Country/Region', 'Lat', 'Long']

DB_HOST = os.getenv('DB_HOST') or 'localhost'
DB_PORT = 8086

def _format_url(file):
    github = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series"
    return f'{github}/{file}'


def _download(files = SERIES.values()):

    for filename in files:
        url = _format_url(filename)
        resp = requests.get(url)

        if resp.status_code == 200:
            with open(filename, 'wb') as f:
                for chunk in resp:
                    f.write(chunk)


def import_data(series_name):

    url = _format_url(SERIES[series_name])
    df = pd.read_csv(url)
    df2 = df.melt(id_vars=TAG_COLS)
    df2.rename(columns={'variable': 'date', 'value': series_name}, inplace=True)
    df2['date'] = pd.to_datetime(df2['date'])
    df2.set_index('date', inplace=True)
    return df2


def get_influxdb(dbname = 'covid'):
    client = DataFrameClient(host=DB_HOST, port=DB_PORT, database=dbname)
    client.create_database(dbname)
    return client

def reset_db():
    db = get_influxdb()
    for series in SERIES.keys():
        db.drop_measurement(series)

def refresh_data():
    db = get_influxdb()
    for series_name in SERIES.keys():
        df = import_data(series_name)
        db.write_points(df, series_name, tag_columns=TAG_COLS)
        print(f'Refreshed data for series = {series_name}')

if __name__ == '__main__':

    while True:
        time.sleep(10)
        try:
            refresh_data()
            time.sleep(30000)
        except:
            print('Error refreshing db. Will retry in a bit')
            time.sleep(30)