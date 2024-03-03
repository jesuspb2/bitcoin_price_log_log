import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter


def fetch_historical_data(coin_id='bitcoin', vs_currency='usd'):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {
        'vs_currency': vs_currency,
        'days': 'max',  # 'max' for all available history
        'interval': 'daily',  # Daily data
    }
    response = requests.get(url, params=params)
    data = response.json()
    prices = data['prices']
    df = pd.DataFrame(prices, columns=['timestamp', 'price'])
    df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.drop('timestamp', axis=1, inplace=True)
    return df


def read_csv_data(filepath):
    df_csv = pd.read_csv(filepath)
    df_csv['date'] = pd.to_datetime(df_csv['date'], errors='coerce', format='%Y-%m-%d')
    df_csv.dropna(subset=['date'], inplace=True)
    return df_csv


def combine_data(df_api, df_csv):
    df_combined = pd.concat([df_api, df_csv], ignore_index=True)
    df_combined.sort_values('date', inplace=True)
    return df_combined


def readable_formatter(value, pos):
    if value >= 1e6:
        val_str = '{:.0f}M'.format(value/1e6)
    elif value >= 1e3:
        val_str = '{:.0f}K'.format(value/1e3)
    else:
        val_str = str(int(value))
    return val_str


# Fetch data from the API
df_api_data = fetch_historical_data()

# Read data from the CSV
df_csv_data = read_csv_data('price_bitcoin_early.csv')

# Combine the data
df_combined_data = combine_data(df_api_data, df_csv_data)

# Convert dates to the number of days since 2009-01-03
base_date = pd.to_datetime('2009-01-03')
df_combined_data['days_since_base'] = (df_combined_data['date'] - base_date).dt.days

# Extend the lines
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

# Plotting
plt.figure(figsize=(10, 5))
plt.plot(df_combined_data['days_since_base'],
         df_combined_data['price'],
         label='Bitcoin Price',
         color='blue',
         alpha=0.5)
plt.plot(np.append(df_combined_data['days_since_base'].values, future_days),
         y_fit,
         label='Fit Line',
         color='red',
         linestyle='--')
plt.plot(np.append(df_combined_data['days_since_base'].values, future_days),
         y_fit_down,
         label='Fit Line Displaced',
         color='green',
         linestyle='--')
plt.plot(np.append(df_combined_data['days_since_base'].values, future_days),
         y_fit_up,
         label='Fit Line Displaced',
         color='green',
         linestyle='--')
plt.xscale('log')
plt.yscale('log')
desired_ticks = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000]
plt.xticks(desired_ticks, [readable_formatter(i, None) for i in desired_ticks])
plt.xlabel('Days since Coinbase (2009-01-03)')
plt.ylabel('Price (USD)')
plt.title('Bitcoin Price (Log-Log Scale)')
plt.gca().xaxis.set_major_formatter(FuncFormatter(readable_formatter))
plt.gca().yaxis.set_major_formatter(FuncFormatter(readable_formatter))
plt.legend()
plt.grid(True, which="both", ls="--")
plt.show()
