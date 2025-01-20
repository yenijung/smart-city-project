import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense, TimeDistributed, RepeatVector, Input
from keras.optimizers import RMSprop, Adam, SGD, Adagrad, Adadelta, Adamax, Nadam
from keras_tuner import HyperModel, BayesianOptimization, Objective
from keras.callbacks import EarlyStopping

np.random.seed(42)
tf.random.set_seed(42)

# load training dataset
df_train = pd.read_csv('Datasets/preprocessed_weather_combined.csv')
# load validation dataset
df_validation = pd.read_csv('Datasets/weather_validation1.csv')
# load testing dataset
df_test = pd.read_csv('Datasets/weather_test.csv')
# load the functions defined in raw_to_input_led.py
n_forecast = 96
from raw_to_input_weather import convert_to_2d_table, prepare_y_many_to_many, convert_to_3d_table

'''
Hyperparameters:
1. time_steps: 96, 100, ... , 192
2. batch_size: 16, 32, 64, 128
3. learning_rate: 0.001, 0.01
4. units: 50, 60, ... , 100
5. optimizer: RMSprop, Adam, SGD, Adagrad, Adadelta, Adamax, Nadam

Fixed parameters:
1. features: 11
2. n_forecast: 96
'''

def prepare_dataset(df_train, df_validation, time_steps, n_forecast):
    pivot_df_train, sc_train = convert_to_2d_table(df_train)
    y_train = prepare_y_many_to_many(pivot_df_train, time_steps, n_forecast)
    x_train, total_samples_train, features_train = convert_to_3d_table(pivot_df_train, time_steps, n_forecast)

    pivot_df_val, sc_val = convert_to_2d_table(df_validation)
    y_val = prepare_y_many_to_many(pivot_df_val, time_steps, n_forecast)
    x_val, total_samples_val, features_val = convert_to_3d_table(pivot_df_val, time_steps, n_forecast)

    return x_train, y_train, x_val, y_val, sc_train, sc_val

class HyperModel_weather(HyperModel):
    def __init__(self, df_train, df_validation, features, n_forecast):
        self.features = features
        self.n_forecast = n_forecast
        self.df_train = df_train
        self.df_validation = df_validation

    def build(self, hp):
        time_steps = hp.Int('time_steps', min_value=96, max_value=192, step=4)
        learning_rate = hp.Choice('learning_rate', values=[0.001, 0.01])
        units = hp.Choice('units', values=[50, 60, 70, 80, 90, 100])
        num_layers = hp.Int('num_layers', min_value=1, max_value=4, step=1)
        optimizer_choice = hp.Choice('optimizer', values=['RMSprop', 'Adam', 'SGD', 'Adagrad', 'Adadelta', 'Adamax', 'Nadam'])

        x_train, y_train, x_val, y_val, sc_train, sc_val = prepare_dataset(self.df_train, self.df_validation, time_steps, self.n_forecast)

        self.train_data = (x_train, y_train)
        self.val_data = (x_val, y_val)

        # LSTM architecture
        lstm_model = Sequential()
        lstm_model.add(Input(shape=(time_steps, self.features)))

        # Adding multiple LSTM layers based on the hyperparameter num_layers
        for i in range(num_layers):
            return_sequences = True if i < num_layers - 1 else False
            lstm_model.add(LSTM(units=units,
                                return_sequences=return_sequences))

        lstm_model.add(RepeatVector(self.n_forecast))

        for _ in range(num_layers):
            lstm_model.add(LSTM(units=units,
                                return_sequences=True))

        lstm_model.add(TimeDistributed(Dense(self.features)))

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

        lstm_model.compile(optimizer=optimizer, loss='mse')
        return lstm_model

    def fit(self, hp, model, *args, **kwargs):
        batch_size = hp.Choice('batch_size', values=[16, 32, 64, 128])
        x_train, y_train = self.train_data
        x_val, y_val = self.val_data
        return model.fit(
            x_train, y_train,
            validation_data=(x_val, y_val),
            batch_size=batch_size,
            *args, **kwargs
        )


hypermodel = HyperModel_weather(df_train, df_validation, features=11, n_forecast=96)
tuner = BayesianOptimization(
    hypermodel,
    objective=Objective('val_loss', direction='min'),
    max_trials=15,
    directory='weather_opt',
    project_name='weather_opt'
)

tuner.search(epochs=50)


trials = tuner.oracle.get_trial()
for trial in trials.values():
    print(f"Trial {trial.trial_id}:\n"
          f"  - time_steps: {trial.hyperparameters.values['time_steps']}\n"
          f"  - batch_size: {trial.hyperparameters.values['batch_size']}\n"
          f"  - learning_rate: {trial.hyperparameters.values['learning_rate']}\n"
          f"  - units: {trial.hyperparameters.values['units']}\n"
          f"  - optimizer: {trial.hyperparameters.values['optimizer']}\n"
          f"  - Validation Loss: {trial.score}\n")

best_hyperparameters = tuner.get_best_hyperparameters(num_trials=1)[0]

print(best_hyperparameters)

# Save the best hyperparameters
with open('Models/best_hyperparameters_weather.txt', 'w') as f:
    f.write("Best Hyperparameters:\n")
    for param, value in best_hyperparameters.values.items():
        f.write(f"{param}: {value}\n")
    f.write(f"Validation Loss: {tuner.oracle.get_trial(best_hyperparameters.trial_id).score}\n")
