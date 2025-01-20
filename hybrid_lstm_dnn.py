import numpy as np
import pandas as pd
import tensorflow as tf
from keras.models import Model
from keras.layers import Input, LSTM, Dense, Concatenate
from keras.optimizers import Adam

from hyperparam_tuning_integrated import prepare_led, prepare_weather
from lstm_led import build_model as build_led_model
from lstm_weather import build_model as build_weather_model

np.random.seed(42)
tf.random.set_seed(42)

def build_hybrid_model(ts_led, features_led, ts_weather, features_weather, output_dim):
    # Define input layers
    led_input = Input(shape=(ts_led, features_led), name='led_input')
    lstm_led = LSTM(90, return_sequences=False, name='lstm_led')(led_input)

    weather_input = Input(shape=(ts_weather, features_weather), name='weather_input')
    lstm_weather = LSTM(50, return_sequences=False, name='lstm_weather')(weather_input)

    # Concatenate LSTM outputs
    concat = Concatenate()([lstm_led, lstm_weather])

    # Define Dense layers
    dense1 = Dense(32, activation='relu', name='dense1')(concat)  # Adjusted to 32 units
    dense2 = Dense(output_dim, activation='linear', name='dense2')(dense1)

    # Build the model
    model = Model(inputs=[led_input, weather_input], outputs=dense2)
    # Setup optimizer with specified learning rate
    optimizer = Adam(learning_rate=0.01)  # Learning rate set to 1e-2
    model.compile(optimizer=optimizer, loss='mse')

    return model

# Load LSTM models and weights
model_led = build_led_model(176, 15, 96, 90, 1, 0.001)
model_weather = build_weather_model(124, 11, 96, 50, 1, 0.01)
model_led.load_weights('Models/best_model_led.h5')
model_weather.load_weights('Models/best_model_weather.h5')

# Create the hybrid model
model = build_hybrid_model(176, 15, 124, 11, 720)  # Output dimension set to match the LED data

# Data preparation (assuming these functions are defined as before)
df_train_led = pd.read_csv('Datasets/led_train.csv')
df_train_weather = pd.read_csv('Datasets/weather_train.csv')
df_val_led = pd.read_csv('Datasets/led_validation.csv')
df_val_weather = pd.read_csv('Datasets/weather_validation1.csv')

x_train_led, y_train_led, x_val_led, y_val_led, sc_train_led, sc_val_led = prepare_led(df_train_led, df_val_led, 176, 96)
x_train_weather, y_train_weather, x_val_weather, y_val_weather, sc_train_weather, sc_val_weather = prepare_weather(df_train_weather, df_val_weather, 124, 96)

# Ensure the datasets are aligned
min_samples = min(len(x_train_led), len(x_train_weather), len(y_train_led))
x_train_led = x_train_led[:min_samples]
x_train_weather = x_train_weather[:min_samples]
y_train_led = y_train_led[:min_samples]

# Model training
model.fit([x_train_led, x_train_weather], y_train_led, epochs=10, batch_size=32)

# Save the model
model.save('Models/hybrid_lstm_dnn.h5')
