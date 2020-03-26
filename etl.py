import requests
import time
import os
import sys
import pandas as pd
from influxdb import DataFrameClient
import yfinance as yf
from covid import CovidEtl
from market import MarketEtl

DB_HOST = os.getenv('DB_HOST') or 'localhost'
DB_PORT = 8086

def get_influxdb(dbname = 'covid'):
    client = DataFrameClient(host=DB_HOST, port=DB_PORT, database=dbname)
    client.create_database(dbname)
    return client


def import_covid_data():
    covid_etl = CovidEtl(get_influxdb('covid'))
    covid_etl.refresh_data()


def import_market_data():
    market_etl = MarketEtl(get_influxdb('market'))
    market_etl.refresh_data()


if __name__ == '__main__':

    while True:
        try:
            import_covid_data()
            import_market_data()
            time.sleep(3600)
        except:
            print('Error refreshing db. Will retry in a bit')
            print(sys.exc_info())
            time.sleep(10)