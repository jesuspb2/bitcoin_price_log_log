import numpy as np
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


def define_object_bitcoin():
    fetcher = DataFetcher(filepath='../price_bitcoin_early.csv')
    df_api_data = fetcher.fetch_historical_data()
    df_csv_data = fetcher.read_csv_data()
    analyzer = DataAnalyzer()
    df_combined_data = analyzer.combine_data(df_api_data, df_csv_data)
    analyzer.prepare_data(df_combined_data)

    return df_combined_data


def calculate_fit_line(df_combined_data):
    max_days_since_base = df_combined_data['days_since_base'].max()
    future_days = np.arange(max_days_since_base, max_days_since_base + 3500)
    x_log = np.log(np.append(df_combined_data['days_since_base'].values, future_days))
    x_future_log = np.log(future_days)
    y_log = np.log(df_combined_data['price'])
    slope, intercept = np.polyfit(x_log[:len(df_combined_data)], y_log, 1)
    y_fit = np.exp(intercept) * np.exp(x_log * slope)
    new_intercept = intercept + 0.9
    y_fit_up = np.exp(new_intercept) * np.exp(x_log * slope)
    new_intercept = intercept - 0.9
    y_fit_down = np.exp(new_intercept) * np.exp(x_log * slope)

    return future_days, y_fit, y_fit_down, y_fit_up
