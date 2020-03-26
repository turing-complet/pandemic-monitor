import pandas as pd
from influxdb import DataFrameClient
import yfinance as yf

class MarketEtl:

    # pass in influxdb client
    def __init__(self, client):
        self.client = client


    def import_data(self):
        spy = yf.Ticker('SPY')
        dh = spy.history(period='ytd')
        dh.drop(columns=['Volume', 'Dividends', 'Stock Splits'], inplace=True)
        return dh
    

    def refresh_data(self):
        df = self.import_data()
        self.client.write_points(df, 'spy')
        print(f'Refreshed data for series = spy')