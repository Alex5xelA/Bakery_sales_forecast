import lightgbm as lgb
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from darts import TimeSeries
from darts.models import NBEATSModel
from darts.utils.missing_values import fill_missing_values

# load dataset
ds_path = 'raw_data/final_dataset.csv'
df = pd.read_csv(ds_path)

# target col
series = TimeSeries.from_dataframe(df, [['index', 'traditional_baguette']])

# split the data into training and testing sets
train, test = series.split_after(0.8)

# create lightgbm dataset
train_data = lgb.Dataset(train.pd_dataframe().drop(columns=['traditional_baguette']), label=train.pd_dataframe()['traditional_baguette'])
test_data = lgb.Dataset(test.pd_dataframe().drop(columns=['traditional_baguette']), label=test.pd_dataframe()['traditional_baguette'], reference=train_data)

# set hyperparameters
params = {
    'objective': 'binary',
    'metric': 'binary_logloss',
    'boosting_type': 'gbdt',
    'num_leaves': 31,
    'learning_rate': 0.05,
    'feature_fraction': 0.9
}

# train the lightgbm model
num_round = 100
bst = lgb.train(params, train_data, num_round, valid_sets=[test_data], early_stopping_rounds=10)

# make predictions on the test set
y_pred = bst.predict(test.pd_dataframe().drop(columns=['traditional_baguette']), num_iteration=bst.best_iteration)
y_pred_binary = np.round(y_pred)

# convert the lightgbm predictions to a darts timeseries
lgb_predictions = TimeSeries.from_dataframe(test.pd_dataframe(), pd.Series(y_pred_binary, name='traditional_baguette'))

# evaluate the accuracy
accuracy = accuracy_score(test.pd_dataframe()['traditional_baguette'], y_pred_binary)
print(f"accuracy: {accuracy}")

# plot the true values and lightgbm predictions
test.plot(label='true values')
lgb_predictions.plot(label='lightgbm predictions')
