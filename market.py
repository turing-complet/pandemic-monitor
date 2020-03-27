import pandas as pd
from influxdb import DataFrameClient
import yfinance as yf

SERIES = ['SPY', 'VIXY']

class MarketEtl:

    # pass in influxdb client
    def __init__(self, client):
        self.client = client


    def import_data(self, ticker):
        asset = yf.Ticker(ticker)
        dh = asset.history(period='ytd')
        dh.drop(columns=['Volume', 'Dividends', 'Stock Splits'], inplace=True)
        return dh
    

    def refresh_data(self):
        for ticker in SERIES:
            df = self.import_data(ticker)
            self.client.write_points(df, ticker.lower())
            print(f'Refreshed data for series = {ticker.lower()}')