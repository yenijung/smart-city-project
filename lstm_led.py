"""
We will use the LSTM model and GRU model to predict the LED light intensity.
After that, we will compare the performance of these two models to choose the best one.
Evaluation: MSE, MAE, R-Squared
In this snippet, we will use the LSTM model.
1. Normalize the 'Usage' column
2. Convert the 'Start Date Time' column to datetime
3. Set 'Start Date Time' as the index
4. As there is 15 different locations, this data will be considered as a multivariate time series data.
   To make this data as a multivariate time series data, at each time stage,
   it should be reconfigured in the form of a matrix that contains the Usage values for all regions;
   for each 'Start Date Time', a data structure that simultaneously considers the Usage values
   for all Locs measured at that time should be created = data pivoting
"""
import pandas as pd
from keras.models import Sequential
from keras.layers import LSTM, Dense, TimeDistributed, RepeatVector, Input
from keras.optimizers import Adam
import tensorflow as tf
import numpy as np
from keras.callbacks import EarlyStopping

np.random.seed(42)
tf.random.set_seed(42)

# load training dataset
df_train = pd.read_csv('Datasets/led_train.csv')
# load validation dataset
df_validation = pd.read_csv('Datasets/led_validation.csv')
# load the functions defined in raw_to_input_led.py
from raw_to_input_led import convert_to_2d_table, prepare_y_many_to_many, convert_to_3d_table

# Prepare the dataset for the LSTM model
def prepare_dataset(df_train, df_validation, time_steps, n_forecast):
    pivot_df_train, sc_train = convert_to_2d_table(df_train)
    y_train = prepare_y_many_to_many(pivot_df_train, time_steps, n_forecast)
    x_train, total_samples_train, features_train = convert_to_3d_table(pivot_df_train, time_steps, n_forecast)

    pivot_df_val, sc_val = convert_to_2d_table(df_validation)
    y_val = prepare_y_many_to_many(pivot_df_val, time_steps, n_forecast)
    x_val, total_samples_val, features_val = convert_to_3d_table(pivot_df_val, time_steps, n_forecast)

    return x_train, y_train, x_val, y_val, sc_train, sc_val

early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

# Based on the hyperparameters, create the LSTM model
def build_model(time_steps, features, n_forecast, units, num_layers, learning_rate):
    model = Sequential()
    model.add(Input(shape=(time_steps, features)))

    # Dynamic LSTM model
    for i in range(num_layers):
        if i < num_layers - 1:
            model.add(LSTM(units=units, return_sequences=True))
        else:
            model.add(LSTM(units=units, return_sequences=False))

    model.add(RepeatVector(n_forecast))

    for _ in range(num_layers):
        model.add(LSTM(units=units, return_sequences=True))

    model.add(TimeDistributed(Dense(features)))

    # Set the optimizer
    optimizer = Adam(learning_rate=learning_rate)
    model.compile(optimizer=optimizer, loss='mse')
    return model


# Based on the hyperparameters, create the LSTM model
time_steps = 176  # Hyperparameter
features = 15  # fixed parameter
n_forecast = 96  # fixed parameter
units = 90  # Hyperparameter
num_layers = 1  # fixed parameter
learning_rate = 0.001  # Hyperparameter
batch_size = 128  # Hyperparameter

x_train, y_train, x_val, y_val, sc1, sc2 = prepare_dataset(df_train, df_validation, time_steps, n_forecast)

# Create the LSTM model
lstm_model = build_model(time_steps, features, n_forecast, units, num_layers, learning_rate)

# # Train the model
# lstm_model.fit(x_train, y_train, validation_data=(x_val, y_val), epochs=50, batch_size=batch_size, verbose=1, callbacks=[early_stopping])
#
# # Save the model
# lstm_model.save('Models/best_model_led.h5')
