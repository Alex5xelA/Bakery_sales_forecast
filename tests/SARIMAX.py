import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

# gen seasonal time series data
np.random.seed(42)
date_rng = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
data = np.random.normal(loc=0, scale=1, size=len(date_rng))
seasonality = 10 * np.sin(2 * np.pi * (date_rng.dayofyear / 365.25))
data_with_seasonality = data + seasonality

# df
df = pd.DataFrame(index=date_rng, data={'y': data_with_seasonality})

# plot data
plt.figure(figsize=(12, 6))
plt.plot(df.index, df['y'], label='Original Data')
plt.title('Time Series Data with Seasonality')
plt.legend()
plt.show()

# plot acf and pacf for sarima model
plot_acf(df['y'], lags=40)
plt.title('Autocorrelation Function (ACF)')
plt.show()

plot_pacf(df['y'], lags=40)
plt.title('Partial Autocorrelation Function (PACF)')
plt.show()

# fit model
order = (1, 0, 1, 12)  # (p, d, q, s) order
model = SARIMAX(df['y'], order=order)
results = model.fit(disp=False)

# forecast future vals
forecast_steps = 30
forecast = results.get_forecast(steps=forecast_steps)

# plot org vals
plt.figure(figsize=(12, 6))
plt.plot(df.index, df['y'], label='Original Data')
plt.plot(forecast.index, forecast.predicted_mean, color='red', label='Forecast')
plt.title('SARIMA Forecast')
plt.legend()
plt.show()
