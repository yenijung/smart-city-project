import pandas as pd
from keras.models import load_model
import tensorflow as tf
import numpy as np
from matplotlib import pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from lstm_weather import build_model

# Based on the hyperparameters, create the LSTM model
time_steps = 124  # Hyperparameter
features = 11  # fixed parameter
n_forecast = 96  # fixed parameter
units = 50  # Hyperparameter
num_layers = 1  # Hyperparameter
learning_rate = 0.01  # Hyperparameter
batch_size = 64  # Hyperparameter

np.random.seed(42)
tf.random.set_seed(42)

model = build_model(time_steps, features, n_forecast, units, num_layers, learning_rate)
model.load_weights('Models/best_model_weather.h5')

# load training dataset
df_train = pd.read_csv('Datasets/weather_train.csv')
df_train2 = pd.read_csv('Datasets/preprocessed_weather2.csv')
# combine the two datasets
combined_train = pd.concat([df_train2, df_train])
# load validation dataset
df_validation = pd.read_csv('Datasets/weather_validation1.csv')
# load the functions defined in raw_to_input_led.py
from raw_to_input_weather import convert_to_2d_table, prepare_y_many_to_many, convert_to_3d_table
def prepare_dataset(df_train, df_validation, time_steps, n_forecast):
    pivot_df_train, sc_train = convert_to_2d_table(df_train)
    y_train = prepare_y_many_to_many(pivot_df_train, time_steps, n_forecast)
    x_train, total_samples_train, features_train = convert_to_3d_table(pivot_df_train, time_steps, n_forecast)

    pivot_df_val, sc_val = convert_to_2d_table(df_validation)
    y_val = prepare_y_many_to_many(pivot_df_val, time_steps, n_forecast)
    x_val, total_samples_val, features_val = convert_to_3d_table(pivot_df_val, time_steps, n_forecast)

    return x_train, y_train, x_val, y_val, sc_train, sc_val

_, _, x_val, y_val, _, sc_val = prepare_dataset(combined_train, df_validation, time_steps=124, n_forecast=96)

prediction = model.predict(x_val)

mse = mean_squared_error(y_val.flatten(), prediction.flatten())
mae = mean_absolute_error(y_val.flatten(), prediction.flatten())
r2 = r2_score(y_val.flatten(), prediction.flatten())

print(f'MSE: {mse}')
print(f'MAE: {mae}')
print(f'R2: {r2}')

# Descaling for the evaluation metrics
def descale(predictions, scaler):
    prediction_reshaped = predictions.reshape(-1, predictions.shape[-1])
    prediction_inv = scaler.inverse_transform(prediction_reshaped)

    return prediction_inv.reshape(predictions.shape)

# Plot the predictions
plt.figure(figsize=(20, 10))
plt.plot(y_val[0, :, 0], label='Actual', marker='o', linestyle='-', color='blue')
plt.plot(prediction[0, :, 0], label='Prediction', marker='x', linestyle='--', color='red')

feature_names = combined_train.columns.tolist()

def plot_predictions(predictions, actuals, scaler, features):
    # Descale the predictions and actual values
    predictions_descaled = descale(predictions, scaler)
    actuals_descaled = descale(actuals, scaler)

    # Iterate through each feature
    for i in range(features):
        plt.figure(figsize=(10, 5))
        # Plotting the actual values
        plt.plot(actuals_descaled[0, :, i], label=f'Actual {feature_names[i]}', marker='o')
        # Plotting the predicted values
        plt.plot(predictions_descaled[0, :, i], label=f'Predicted {feature_names[i]}', marker='x', linestyle='--')
        plt.title(f'Comparison of Actual and Predicted Values for {feature_names[i]}')
        plt.xlabel('Time Steps')
        plt.ylabel(f'{feature_names[i]} Value')
        plt.legend()
        plt.grid(True)
        plt.savefig(f'Images/weather_lstm_prediction/{feature_names[i]}.png')
        plt.show()

plot_predictions(prediction, y_val, sc_val, features)
