import requests
import pandas as pd


class DataFetcher:
    def __init__(self, coin_id='bitcoin', vs_currency='usd', filepath=None):
        self.coin_id = coin_id
        self.vs_currency = vs_currency
        self.filepath = filepath

    def fetch_historical_data(self):
        url = f"https://api.coingecko.com/api/v3/coins/{self.coin_id}/market_chart"
        params = {
            'vs_currency': self.vs_currency,
            'days': 'max',
            'interval': 'daily',
        }
        response = requests.get(url, params=params)
        data = response.json()
        prices = data['prices']
        df = pd.DataFrame(prices, columns=['timestamp', 'price'])
        df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.drop('timestamp', axis=1, inplace=True)
        return df

    def read_csv_data(self):
        df_csv = pd.read_csv(self.filepath)
        df_csv['date'] = pd.to_datetime(df_csv['date'], errors='coerce', format='%Y-%m-%d')
        df_csv.dropna(subset=['date'], inplace=True)
        return df_csv


class DataAnalyzer:
    @staticmethod
    def combine_data(df_api, df_csv):
        df_combined = pd.concat([df_api, df_csv], ignore_index=True)
        df_combined.sort_values('date', inplace=True)
        return df_combined

    @staticmethod
    def prepare_data(df_combined):
        base_date = pd.to_datetime('2009-01-03')
        df_combined['days_since_base'] = (df_combined['date'] - base_date).dt.days
        return df_combined


class DataVisualizer:
    @staticmethod
    def readable_formatter(value, pos):
        if value >= 1e6:
            val_str = '{:.0f}M'.format(value / 1e6)
        elif value >= 1e3:
            val_str = '{:.0f}K'.format(value / 1e3)
        else:
            val_str = str(int(value))
        return val_str
