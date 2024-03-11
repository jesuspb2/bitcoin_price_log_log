import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import FuncFormatter
from bitcoin_price_common import DataVisualizer, define_object_bitcoin, calculate_fit_line

df_combined_data = define_object_bitcoin()
visualizer = DataVisualizer()
future_days, y_fit, y_fit_down, y_fit_up = calculate_fit_line(df_combined_data)

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
