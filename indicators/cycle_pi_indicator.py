import numpy as np
from matplotlib import pyplot as plt
from bitcoin_price_common import DataFetcher, DataAnalyzer


def calculate_pi_cycle_indicator(df):
    df['moving_average_111'] = df['price'].rolling(window=111).mean()
    df['moving_average_350_x_2'] = df['price'].rolling(window=350).mean() * 2
    return df


def find_pi_cycle_crossovers(df):
    df['ma_difference'] = df['moving_average_111'] - df['moving_average_350_x_2']
    df['crossover'] = (df['ma_difference'].apply(np.sign) * df['ma_difference'].shift(1).apply(np.sign) < 0)
    crossover_points = df[df['crossover']]
    return crossover_points[['date', 'moving_average_111', 'moving_average_350_x_2']]


def plot_cycle_pi():

    fetcher = DataFetcher(filepath='../price_bitcoin_early.csv')
    df_api_data = fetcher.fetch_historical_data()
    df_csv_data = fetcher.read_csv_data()
    analyzer = DataAnalyzer()
    df_combined_data = analyzer.combine_data(df_api_data, df_csv_data)
    df_combined_data = calculate_pi_cycle_indicator(df_combined_data)
    crossover_points = find_pi_cycle_crossovers(df_combined_data)

    plt.figure(figsize=(10, 5))
    plt.plot(df_combined_data['date'],
             df_combined_data['price'],
             label='Bitcoin Price',
             color='blue',
             alpha=0.5)
    plt.plot(df_combined_data['date'], df_combined_data['moving_average_111'], label='111DMA', color='orange', alpha=0.75)
    plt.plot(df_combined_data['date'], df_combined_data['moving_average_350_x_2'], label='350DMA x 2', color='green', alpha=0.75)
    for index, row in crossover_points.iterrows():
        plt.plot(row['date'], row['moving_average_111'], 'ro')  # 'ro' creates red dots

    plt.yscale('log')
    plt.xlabel('Days since Coinbase (2009-01-03)')
    plt.ylabel('Price (USD)')
    plt.title('Bitcoin Price (Log-Lineal Scale)')
    plt.legend()
    plt.grid(True, which="both", ls="--")
    plt.show()
