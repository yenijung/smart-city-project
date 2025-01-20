"""
[LSTM-DNN Hybrid Model for LED and Weather Data]
1) Load best lstm models for led and weather data
2) Get the predictions from the models
3) Reformat and concat them for dnn input
4) Hyperparameter tuning for dnn
"""

import pandas as pd
import tensorflow as tf
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Concatenate, Lambda, LSTM
from keras import backend as K, Input
from kerastuner.tuners import BayesianOptimization
from keras.models import Model
from keras.optimizers import Adam, RMSprop, SGD, Adagrad, Adadelta, Adamax, Nadam

from lstm_led import build_model as build_led_model
from lstm_weather import build_model as build_weather_model

np.random.seed(42)
tf.random.set_seed(42)

# Load the best lstm models for led and weather
model_led = build_led_model(176, 15, 96, 90, 1, 0.001)
model_led.load_weights('Models/best_model_led.h5')

model_weather = build_weather_model(124, 11, 96, 50, 1, 0.01)
model_weather.load_weights('Models/best_model_weather.h5')

# Load the data for led and weather
df_train_led = pd.read_csv('Datasets/led_train.csv')
df_val_led = pd.read_csv('Datasets/led_validation.csv')
df_train_weather = pd.read_csv('Datasets/weather_train.csv')
df_val_weather = pd.read_csv('Datasets/weather_validation1.csv')

# Initialize models with data
x_init_led = np.random.rand(1, 176, 15)
x_init_weather = np.random.rand(1, 124, 11)

# Make a dummy prediction to initialize models
_ = model_led.predict(x_init_led)
_ = model_weather.predict(x_init_weather)

# Prepare the data for led and weather
# ts_led and ts_weather here will be set through hyperparam_tuning_led.py and hyperparam_tuning_weather.py
# n_forecast is set to 96 (lstm model's n_forecast)
def prepare_led(df_train, df_validation, ts_led, n_forecast):
    from raw_to_input_led import convert_to_2d_table, prepare_y_many_to_many, convert_to_3d_table
    pivot_df_train, sc_train = convert_to_2d_table(df_train)
    y_train = prepare_y_many_to_many(pivot_df_train, ts_led, n_forecast)
    x_train, total_samples_train, features_train = convert_to_3d_table(pivot_df_train, ts_led, n_forecast)

    pivot_df_val, sc_val = convert_to_2d_table(df_validation)
    y_val = prepare_y_many_to_many(pivot_df_val, ts_led, n_forecast)
    x_val, total_samples_val, features_val = convert_to_3d_table(pivot_df_val, ts_led, n_forecast)

    return x_train, y_train, x_val, y_val, sc_train, sc_val

def prepare_weather(df_train, df_validation, ts_weather, n_forecast):
    from raw_to_input_weather import convert_to_2d_table, prepare_y_many_to_many, convert_to_3d_table
    pivot_df_train, sc_train = convert_to_2d_table(df_train)
    y_train = prepare_y_many_to_many(pivot_df_train, ts_weather, n_forecast)
    x_train, total_samples_train, features_train = convert_to_3d_table(pivot_df_train, ts_weather, n_forecast)

    pivot_df_val, sc_val = convert_to_2d_table(df_validation)
    y_val = prepare_y_many_to_many(pivot_df_val, ts_weather, n_forecast)
    x_val, total_samples_val, features_val = convert_to_3d_table(pivot_df_val, ts_weather, n_forecast)

    return x_train, y_train, x_val, y_val, sc_train, sc_val


x_train_led, y_train_led, x_val_led, y_val_led, sc_train_led, sc_val_led = prepare_led(df_train_led, df_val_led, 176, 96)
x_train_weather, _, x_val_weather, _, _, _ = prepare_weather(df_train_weather, df_val_weather, 124, 96)

print("x_train_led samples:", x_train_led.shape[0])
print("x_train_weather samples:", x_train_weather.shape[0])
print("y_train_led samples:", y_train_led.shape[0])
min_samples = min(x_train_led.shape[0], x_train_weather.shape[0], y_train_led.shape[0])
x_train_led = x_train_led[:min_samples]
x_train_weather = x_train_weather[:min_samples]
y_train_led = y_train_led[:min_samples]
print("Adjusted x_train_led samples:", x_train_led.shape[0])
print("Adjusted x_train_weather samples:", x_train_weather.shape[0])
print("Adjusted y_train_led samples:", y_train_led.shape[0])


def resize_output(y_data, target_steps=48, features=15):
    # y_data: [samples, 96, 15], target_steps: 48
    sample_size, time_steps, features = y_data.shape
    resized_y = np.zeros((sample_size, target_steps, features))

    for i in range(sample_size):
        for j in range(target_steps):
            start_idx = 2 * j
            end_idx = start_idx + 2
            resized_y[i, j, :] = np.mean(y_data[i, start_idx:end_idx, :], axis=0)

    return resized_y


y_train_resized = resize_output(y_train_led, 48)
y_val_resized = resize_output(y_val_led, 48)

print("y_train_resized shape:", y_train_resized.shape)
print("y_val_resized shape:", y_val_resized.shape)

def sequence_to_average(input_sequence):
    return K.mean(input_sequence, axis=1)

# LED lstm
input_shape_led = (176, 15)
input_led = Input(shape=input_shape_led)
output_led = LSTM(90, return_sequences=True)(input_led)
output_led_average = Lambda(lambda x: tf.reduce_mean(x, axis=1), output_shape=(90,))(output_led)

# Weather lstm
input_shape_weather = (124, 11)
input_weather = Input(shape=input_shape_weather)
output_weather = LSTM(50, return_sequences=True)(input_weather)
output_weather_average = Lambda(lambda x: tf.reduce_mean(x, axis=1), output_shape=(50,))(output_weather)

# Concatenate the two outputs
combined = Concatenate()([output_led_average, output_weather_average])
model_led = Model(inputs=input_led, outputs=output_led)
model_weather = Model(inputs=input_weather, outputs=output_weather)

def hybrid_model(hp):
    # Final hybrid model for DNN
    dnn_units = hp.Int('units', min_value=32, max_value=512, step=32)
    dnn_output = Dense(dnn_units, activation='relu')(combined)
    final_output = Dense(48, activation='relu')(dnn_output)   # 48 is the target n_forecast -> fixed
    hybrid_model = Model(inputs=[input_led, input_weather], outputs=final_output)

    # Compile the model
    learning_rate = hp.Choice('learning_rate', values=[1e-2, 1e-3, 1e-4])
    optimizer_choice = hp.Choice('optimizer',
                                 values=['RMSprop', 'Adam', 'SGD', 'Adagrad', 'Adadelta', 'Adamax', 'Nadam'])
    optimizer_dict = {
        'RMSprop': RMSprop(learning_rate=learning_rate),
        'Adam': Adam(learning_rate=learning_rate),
        'SGD': SGD(learning_rate=learning_rate),
        'Adagrad': Adagrad(learning_rate=learning_rate),
        'Adadelta': Adadelta(learning_rate=learning_rate),
        'Adamax': Adamax(learning_rate=learning_rate),
        'Nadam': Nadam(learning_rate=learning_rate)
    }
    optimizer = optimizer_dict[optimizer_choice]

    hybrid_model.compile(optimizer=optimizer, loss='mse', metrics=['mse'])
    return hybrid_model

# Hyperparameter tuning
tuner = BayesianOptimization(hybrid_model,
                             objective='val_loss',
                             max_trials=20,
                             executions_per_trial=2,
                             directory='Models',
                             project_name='hybrid_model')

tuner.search([x_train_led, x_train_weather], y_train_led,
                validation_data=([x_val_led, x_val_weather], y_val_led),
                epochs=50,
                batch_size=32)

# Get the best model
best_hyperparameters = tuner.get_best_hyperparameters(num_trials=1)[0]

print(best_hyperparameters)

# Save the best hyperparameters
with open('Models/best_hyperparameters_hybrid.txt', 'w') as f:
    f.write("Best Hyperparameters:\n")
    for param, value in best_hyperparameters.values.items():
        f.write(f"{param}: {value}\n")
    f.write(f"Validation Loss: {tuner.oracle.get_trial(best_hyperparameters.trial_id).score}\n")
