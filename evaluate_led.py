import pandas as pd
from keras.models import load_model
import tensorflow as tf
import numpy as np
from matplotlib import pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from lstm_led import build_model


# Based on the hyperparameters, create the LSTM model
time_steps = 176  # Hyperparameter
features = 15  # fixed parameter
n_forecast = 48  # fixed parameter
units = 90  # Hyperparameter
num_layers = 1  # fixed parameter
learning_rate = 0.001  # Hyperparameter
batch_size = 128  # Hyperparameter

model = build_model(time_steps, features, n_forecast, units, num_layers, learning_rate)
model.load_weights('Models/best_model_led.h5')

np.random.seed(42)
tf.random.set_seed(42)

# load training dataset
df_train = pd.read_csv('Datasets/led_train.csv')
# load validation dataset
df_validation = pd.read_csv('Datasets/led_validation.csv')
# load test dataset
df_test = pd.read_csv('Datasets/led_test.csv')
# load the functions defined in raw_to_input_led.py
from raw_to_input_led import convert_to_2d_table, prepare_y_many_to_many, convert_to_3d_table
def prepare_dataset(df_train, df_validation, time_steps, n_forecast):
    pivot_df_train, sc_train = convert_to_2d_table(df_train)
    y_train = prepare_y_many_to_many(pivot_df_train, time_steps, n_forecast)
    x_train, total_samples_train, features_train = convert_to_3d_table(pivot_df_train, time_steps, n_forecast)

    pivot_df_val, sc_val = convert_to_2d_table(df_validation)
    y_val = prepare_y_many_to_many(pivot_df_val, time_steps, n_forecast)
    x_val, total_samples_val, features_val = convert_to_3d_table(pivot_df_val, time_steps, n_forecast)

    return x_train, y_train, x_val, y_val, sc_train, sc_val

_, _, x_val, y_val, _, sc_val = prepare_dataset(df_train, df_validation, time_steps=176, n_forecast=48)

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


def plot_predictions(predictions, actuals, scaler, features):
    # Descale the predictions and actual values
    predictions_descaled = descale(predictions, scaler)
    actuals_descaled = descale(actuals, scaler)

    # Iterate through each feature
    for i in range(features):
        plt.figure(figsize=(10, 5))
        # Plotting the actual values
        plt.plot(actuals_descaled[0, :, i], label=f'Actual value', marker='o')
        # Plotting the predicted values
        plt.plot(predictions_descaled[0, :, i], label=f'Predicted value', marker='x', linestyle='--')
        plt.title(f'Final comparison of Actual and Predicted Values by hybrid model for Location {i+1}')
        plt.xlabel('Time Steps')
        plt.ylabel(f'Usage')
        plt.legend()
        plt.grid(True)
        # save the plot
        plt.savefig(f'Images/test_result/led_location_{i+1}.png')
        plt.show()

plot_predictions(prediction, y_val, sc_val, features)


