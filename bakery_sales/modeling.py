import pandas as pd
import numpy as np
from datetime import datetime
from bakery_sales.preprocessor import preprocess

from darts import TimeSeries

def prediction(sales_file, weather_file, model):
    sales_file_preprocessed = preprocess(sales_file)
    data_target = sales_file_preprocessed
    df_weather = weather_file
    
    datetime.strptime(df_weather['time'][4], '%Y-%m-%dT%H:%M')
    df_weather['timestamp'] = df_weather['time'].apply(lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M'))

    # Creating day of week as a cyclical feature
    # First, create the day of the week as a numerical feature
    df_weather['day_of_week'] = pd.to_datetime(df_weather['timestamp']).dt.weekday
    # Since we have a 7 days week period (e.g., days in a week)
    period = 7

    # Convert 'day_of_week' to radians
    df_weather['day_of_week_radians'] = 2 * np.pi * df_weather['day_of_week'] / period

    # Create new features using sine and cosine
    df_weather['day_of_week_sin'] = np.sin(df_weather['day_of_week_radians'])
    df_weather['day_of_week_cos'] = np.cos(df_weather['day_of_week_radians'])
    # Dropping ['month_radians']
    df_weather.drop(columns=['day_of_week_radians', 'day_of_week'], inplace=True)
    # Drops old DATE column
    df_weather = df_weather.drop(columns=['time'])
    # Creates cyclical month feature according to the date
    df_weather['month'] = df_weather.timestamp.dt.month
    # Assuming we have a 12 month period (e.g., month in a year)
    period = 12

    # Convert 'month' to radians
    df_weather['month_radians'] = 2 * np.pi * df_weather['month'] / period

    # Create new features using sine and cosine
    df_weather['month_sin'] = np.sin(df_weather['month_radians'])
    df_weather['month_cos'] = np.cos(df_weather['month_radians'])
    # Dropping ['month_radians']
    df_weather.drop(columns=['month_radians', 'month'], inplace=True)
    # Setting new date column as index
    df_weather.set_index(['timestamp'], inplace=True)
    # Creates dictionary with Holidays
    holidays = [
        '2021-01-01',
        '2021-04-05',
        '2021-05-01',
        '2021-05-08',
        '2021-05-13',
        '2021-05-24',
        '2021-07-14',
        '2021-08-15',
        '2021-11-01',
        '2021-11-11',
        '2021-12-25',
        '2022-01-01',
        '2022-04-18',
        '2022-05-01',
        '2022-05-08',
        '2022-05-26',
        '2022-06-06',
        '2022-07-14',
        '2022-08-15',
    ]
    #holidays = [pd.to_datetime(holiday)for holiday in holidays]
    #df_weather['isHoliday'] = df_weather.index.map(lambda x: 1 if x in holidays else 0)
    df_weather['isHoliday'] = df_weather.index.map(lambda x: 1 if x.strftime('%Y-%m-%d') in holidays else 0)
    # df_weather = df_weather.resample('20min', on = 'timestamp').mean().ffill()

    type(df_weather.index[0].strftime('%Y-%m-%d'))

    merged_data = df_weather.join(data_target, how = 'left')

    final_data = merged_data

    final_data = final_data.fillna(value = 0)

    final_data.reset_index(inplace = True)

    output_chunk_length = 7 * 24 
    print(final_data.columns)
    series = TimeSeries.from_dataframe(final_data[['traditional_baguette']])
    past_covariates = TimeSeries.from_dataframe(final_data[['temperature_2m (°C)', 'relative_humidity_2m (%)', 'rain (mm)', 'wind_speed_100m (km/h)', 'day_of_week_sin', 'day_of_week_cos', 'month_sin', 'month_cos', 'isHoliday']])
    future_covariates = TimeSeries.from_dataframe(final_data[['temperature_2m (°C)', 'relative_humidity_2m (%)', 'rain (mm)', 'wind_speed_100m (km/h)', 'day_of_week_sin', 'day_of_week_cos', 'month_sin', 'month_cos', 'isHoliday']])

    output = model.predict(n = output_chunk_length,
                   series = series,
                   past_covariates = past_covariates,
                   future_covariates = future_covariates)
                   
    output = output.pd_dataframe()

    print("code works ✅")

    return output