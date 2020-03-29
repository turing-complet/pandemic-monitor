import requests
import os
import pandas as pd
from influxdb import DataFrameClient

SERIES = {
    'confirmed': "time_series_covid19_confirmed_global.csv",
    'deaths': "time_series_covid19_deaths_global.csv",
    "recovered": "time_series_covid19_recovered_global.csv"
}

TAG_COLS = ['Province/State', 'Country/Region', 'Lat', 'Long']

class CovidEtl:

    # pass in influxdb client
    def __init__(self, client):
        self.client = client


    def _download(self, files = SERIES.values()):
        for filename in files:
            url = self._format_url(filename)
            resp = requests.get(url)

            if resp.status_code == 200:
                with open(filename, 'wb') as f:
                    for chunk in resp:
                        f.write(chunk)


    def _format_url(self, file):
        github = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series"
        return f'{github}/{file}'


    def import_data(self, series_name):
        url = self._format_url(SERIES[series_name])
        df = pd.read_csv(url)
        df2 = df.melt(id_vars=TAG_COLS)
        df2.rename(columns={'variable': 'date', 'value': series_name}, inplace=True)
        df2['date'] = pd.to_datetime(df2['date'])
        df2.set_index('date', inplace=True)
        return df2


    def reset_db(self):
        for series in SERIES.keys():
            self.client.drop_measurement(series)


    def refresh_data(self):
        for series_name in SERIES.keys():
            df = self.import_data(series_name)
            self.client.write_points(df, series_name, tag_columns=TAG_COLS)
            print(f'Refreshed data for series = {series_name}')