import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import FuncFormatter
from bitcoin_price_common import DataFetcher, DataAnalyzer, DataVisualizer

fetcher = DataFetcher(filepath='../price_bitcoin_early.csv')
df_api_data = fetcher.fetch_historical_data()
df_csv_data = fetcher.read_csv_data()

analyzer = DataAnalyzer()
df_combined_data = analyzer.combine_data(df_api_data, df_csv_data)
df_prepared_data = analyzer.prepare_data(df_combined_data)

visualizer = DataVisualizer()

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
plt.yscale('log')
desired_ticks = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000]
plt.xticks(desired_ticks, [visualizer.readable_formatter(i, None) for i in desired_ticks])
plt.xlabel('Days since Coinbase (2009-01-03)')
plt.ylabel('Price (USD)')
plt.title('Bitcoin Price (Log-Lineal Scale)')
plt.gca().xaxis.set_major_formatter(FuncFormatter(visualizer.readable_formatter))
plt.gca().yaxis.set_major_formatter(FuncFormatter(visualizer.readable_formatter))
plt.legend()
plt.grid(True, which="both", ls="--")
plt.show()
