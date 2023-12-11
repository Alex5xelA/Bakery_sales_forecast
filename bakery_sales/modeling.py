import torch
import pandas as pd
import numpy as np
from datetime import datetime

# specify path to pytorch model .pt file
pt_file_path = 'your_model.pt'

# load pytorch model and set to eval mode
model = torch.load(pt_file_path)
model.eval()


# Importing the dataset
df = pd.DataFrame(pd.read_csv('../raw_data/bakerysales.csv'))

df['date_time'] = df['date'] + ' ' + df['time']
df['date_time'] = pd.to_datetime(df['date_time'])

# Extract the articles and the quantities in order to transform them into column s through a pivot method.
# We'll now have 149 column, one per product with the corresponding qty
pivot = df[['article', 'Quantity']]
products = pivot.pivot(columns = 'article', values = 'Quantity')

# Merge the pivot table with the original dataset and fill the Nan with zeros
# Now for each date point we have the quantity of the article sold
data = df.merge(products, left_index = True, right_index = True)
data = data.fillna(value = 0)

# Keep only the top 7 products (representing 68% of the volume sold)
# Set date as index
data_target = data[['date_time', 'TRADITIONAL BAGUETTE', 'CROISSANT', 'COUPE', 'PAIN AU CHOCOLAT', 'BAGUETTE', 'BANETTE', 'CEREAL BAGUETTE']]
data_target = data_target.resample('60min', on = 'date_time').sum()

data_target = data_target.rename(columns = {'TRADITIONAL BAGUETTE' : 'traditional_baguette',
                                             'CROISSANT' : 'croissant',
                                            'COUPE' : 'coupe',
                                            'PAIN AU CHOCOLAT' : 'pain_au_chocolat',
                                            'BAGUETTE' : 'baguette',
                                            'BANETTE' : 'banette',
                                            'CEREAL BAGUETTE' : 'cereal_baguette'})


# Removing the empty rows
data_target = data_target[data_target != 0]
data_target.dropna(axis = 0, how = 'all', inplace = True)
data_target = data_target.fillna(value = 0)


data_weather = pd.read_csv('../raw_data/open-meteo-paris.csv')

df_weather = data_weather

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

final_data.to_csv('../raw_data/hourly_final_dataset.csv', index = True)

pd.DataFrame(pd.read_csv('../raw_data/hourly_final_dataset.csv'))



