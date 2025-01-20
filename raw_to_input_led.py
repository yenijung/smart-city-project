"""
LED dataset: Start Date Time, Loc, Usage
When this dataset is implemented as a 2D table, each column is the Start Date Time and each row is the Loc, and each cell is the Usage value.
This means that there are (Loc, Usage) pairs per Start Date Time as many as the number of Locs. Therefore, feature=15.
window size (samples) = (total number of datasets) - (time steps) + 1.
The number of time steps was initially set to 4, which may be changed later through verification.
"""

import pandas as pd
import numpy as np

# Load the dataset
df_train = pd.read_csv('Datasets/led_train.csv')
df_val = pd.read_csv('Datasets/led_validation.csv')


# Converting input dataset to 2D Table
# Each column should be Start Date Time and each row should be Loc, and each cell should be a Usage value.
# sc is returned to be used for the inverse transform
def convert_to_2d_table(dataset):
    # Normalize the 'Usage' column
    from sklearn.preprocessing import MinMaxScaler
    sc = MinMaxScaler(feature_range=(0, 1))
    dataset['Usage'] = sc.fit_transform(dataset['Usage'].values.reshape(-1, 1))
    # Convert the 'Start Date Time' column to datetime
    dataset['Start Date Time'] = pd.to_datetime(dataset['Start Date Time'])
    # Set 'Start Date Time' and 'Loc' as the index
    dataset_multi = dataset.set_index(['Start Date Time', 'Loc'])
    # Data pivoting
    pivot_df = dataset_multi.pivot_table(values='Usage', index='Start Date Time', columns='Loc')
    # Fill every NaN value with 0
    pivot_df.fillna(0, inplace=True)
    return pivot_df, sc


# Extract y labels for the many-to-many model
# The number of samples should be the same as the number of samples in the input dataset
# The number of features should be the same as the number of features in the input dataset
def prepare_y_many_to_many(pivot_df, time_steps, n_forecast):
    # The number of samples should be the same as the number of samples in the input dataset
    total_samples = pivot_df.shape[0]
    # The number of features should be the same as the number of features in the input dataset
    features = pivot_df.shape[1]
    y = []
    for i in range(time_steps, total_samples - (n_forecast - 1)):
        y.append(pivot_df.values[i:i + n_forecast])
    y = np.array(y)
    return y


# Convert the 2D table to 3D table
# The number of samples should be the same as the number of samples in the input dataset
# The number of time steps should be the same as the number of time steps in the input dataset
# The number of features should be the same as the number of features in the input dataset
def convert_to_3d_table(pivot_df, time_steps, n_forecast):
    # The number of samples should be the same as the number of samples in the input dataset
    total_samples = pivot_df.shape[0]
    # The number of time steps should be the same as the number of time steps in the input dataset
    features = pivot_df.shape[1]
    x = []
    for i in range(time_steps, total_samples - (n_forecast - 1)):
        x.append(pivot_df.values[i - time_steps:i])
    x = np.array(x)
    return x, total_samples, features


df_train_2d, sc = convert_to_2d_table(df_train)
df_val_2d, sc2 = convert_to_2d_table(df_val)
y_train = prepare_y_many_to_many(df_train_2d, 30, 48)
x_train, total_samples_train, features_train = convert_to_3d_table(df_train_2d, 30, 48)
y_val = prepare_y_many_to_many(df_val_2d, 30, 48)
x_val, total_samples_val, features_val = convert_to_3d_table(df_val_2d, 30, 48)
print("x_train shape: ", x_train.shape)
print("y_train shape: ", y_train.shape)
print("x_val shape: ", x_val.shape)
print("y_val shape: ", y_val.shape)
