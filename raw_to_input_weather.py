import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# Load the dataset
df_train = pd.read_csv('Datasets/preprocessed_weather_combined.csv')
df_val = pd.read_csv('Datasets/weather_validation1.csv')


# Convert input dataset to 2D table with index as 'Start Date Time'
# Each column should be 'Start Date Time' and each row should be a feature, and each cell should be a value.
# sc is returned to be used for the inverse transform
def convert_to_2d_table(dataset):
    # Convert index to datetime
    dataset['Start Date Time'] = pd.to_datetime(dataset['Start Date Time'])
    features = dataset.drop('Start Date Time', axis=1)
    sc = MinMaxScaler(feature_range=(0, 1))
    scaled_features = sc.fit_transform(features)
    dataset_scaled = pd.DataFrame(data=scaled_features, index=dataset['Start Date Time'], columns=features.columns)
    dataset_scaled.fillna(0, inplace=True)
    return dataset_scaled, sc


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
