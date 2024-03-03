import requests
import pandas as pd
import matplotlib.pyplot as plt


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


# Fetch data from the API
df_api_data = fetch_historical_data()

# Read data from the CSV
df_csv_data = read_csv_data('price_bitcoin_early.csv')

# Combine the data
df_combined_data = combine_data(df_api_data, df_csv_data)

# Convert dates to the number of days since 2009-01-03
base_date = pd.to_datetime('2009-01-03')
df_combined_data['days_since_base'] = (df_combined_data['date'] - base_date).dt.days

# Plotting
plt.figure(figsize=(10, 5))
plt.plot(df_combined_data['days_since_base'], df_combined_data['price'], label='Bitcoin Price', color='blue')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Days Since Coinbase (2009-01-03)')
plt.ylabel('Price (USD)')
plt.title('Bitcoin Price (Log-Log Scale)')
plt.legend()
plt.grid(True, which="both", ls="--")
plt.show()