import numpy as np
import pandas as pd
import tensorflow as tf
from keras.models import load_model
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt
from hyperparam_tuning_integrated import prepare_led, prepare_weather

# Set random seed for reproducibility
np.random.seed(42)
tf.random.set_seed(42)

# Load the saved hybrid model
model = load_model('Models/hybrid_lstm_dnn.h5')

def evaluate_model(model, x_led, x_weather, y_true):
    # Make predictions
    predictions = model.predict([x_led, x_weather])

    # Calculate evaluation metrics
    mse = mean_squared_error(y_true.flatten(), predictions.flatten())
    mae = mean_absolute_error(y_true.flatten(), predictions.flatten())
    r2 = r2_score(y_true.flatten(), predictions.flatten())

    return mse, mae, r2, predictions

def plot_predictions(actuals, predictions, title='Model Predictions'):
    num_features = actuals.shape[-1]  # Assumes last dimension is features
    for feature_idx in range(num_features):
        plt.figure(figsize=(10, 5))
        plt.plot(actuals[:, feature_idx], label='Actual Values', color='blue', marker='o')
        plt.plot(predictions[:, feature_idx], label='Predicted Values', color='red', linestyle='--', marker='x')
        plt.title(f'{title} for Location {feature_idx+1}')
        plt.xlabel('Sample Index')
        plt.ylabel('Values')
        plt.legend()
        plt.grid(True)
        plt.show()

# Load datasets
df_train_led = pd.read_csv('Datasets/led_train.csv')
df_train_weather = pd.read_csv('Datasets/weather_train.csv')
df_val_led = pd.read_csv('Datasets/led_validation.csv')
df_val_weather = pd.read_csv('Datasets/weather_validation1.csv')
df_test_led = pd.read_csv('Datasets/led_test.csv')
df_test_weather = pd.read_csv('Datasets/weather_test.csv')

# Prepare validation dataset
x_train_led, y_train_led, x_val_led, y_val_led, sc_train_led, sc_val_led = prepare_led(df_train_led, df_val_led, 176, 96)
x_train_weather, y_train_weather, x_val_weather, y_val_weather, sc_train_weather, sc_val_weather = prepare_weather(df_train_weather, df_val_weather, 124, 96)

# Prepare test dataset
x_test_led, y_test_led, x_test_weather, y_test_weather, sc_test_led, sc_test_weather = prepare_led(df_train_led, df_test_led, 176, 96), prepare_weather(df_train_weather, df_test_weather, 124, 96)

# Ensure the datasets are aligned
min_samples_val = min(len(x_val_led), len(x_val_weather), len(y_val_led))
x_val_led = x_val_led[:min_samples_val]
x_val_weather = x_val_weather[:min_samples_val]
y_val_led = y_val_led[:min_samples_val]

min_samples_test = min(len(x_test_led), len(x_test_weather), len(y_test_led))
x_test_led = x_test_led[:min_samples_test]
x_test_weather = x_test_weather[:min_samples_test]
y_test_led = y_test_led[:min_samples_test]

# Evaluate on validation data
mse_val, mae_val, r2_val, predictions_val = evaluate_model(model, x_val_led, x_val_weather, y_val_led)
print(f'Validation MSE: {mse_val}, MAE: {mae_val}, R2: {r2_val}')

# Evaluate on test data
mse_test, mae_test, r2_test, predictions_test = evaluate_model(model, x_test_led, x_test_weather, y_test_led)
print(f'Test MSE: {mse_test}, MAE: {mae_test}, R2: {r2_test}')

# Plot validation predictions
plot_predictions(y_val_led[0], predictions_val[0], title='Comparisoon of Actual and Predicted Values by Hybrid Model')

# Plot test predictions
plot_predictions(y_test_led[0], predictions_test[0], title='Final comparison of Actual and Predicted Values by hybrid Model')
