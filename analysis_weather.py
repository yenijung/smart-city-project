"""
Before building the VAR model considering seasonality, we would like to see the seasonal pattern of the weather data using:
- AIC and BIC --- 4
- Seasonal Differencing (if there is seasonality, remove it) --- 3
- Time Series Decomposition --- 2
- ADF, Cross analysis (stationarity check) --- 1
- Linear relation (cointegration) --- 1
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.api import VAR
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller, coint
from itertools import combinations
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor


# Load the prepared weather data
weather = pd.read_csv('Datasets/preprocessed_weather_combined.csv', index_col=0, parse_dates=True)
# Make the index into normal column
weather.reset_index(inplace=True)
# Order the columns in alphabetical order
weather = weather.reindex(sorted(weather.columns), axis=1)
# Convert the 'Start Date Time' column into datetime type from object type
weather['Start Date Time'] = pd.to_datetime(weather['Start Date Time'], format='%d/%m/%Y %H:%M:%S')
# Set the 'Start Date Time' column as the index
weather.set_index('Start Date Time', inplace=True)
print(weather)

# AIC and BIC for each parameter to find the best lag for the VAR model
# 'lag' = optimizing the model parameter, determine the model complexity
# The lower the AIC and BIC, the better the model
# TODO: UPDATE - Doesn't have to be done before building the model as it is closer to evaluation, but need to dicuss further if this is further needed.
# TODO: UPDATE2 - This might not be needed so after discussing, this will be removed.
def optimal_lag(data, maxlags=15):
    # Normalize the data
    def normalize(data):
        min = np.min(data, axis=0)
        max = np.max(data, axis=0)
        normalized_data = (data - min) / (max - min)
        return normalized_data
    data = normalize(data)
    # AIC and BIC for each parameter
    aic = []
    bic = []
    for lag in range(1, maxlags + 1):
        model = VAR(data)
        results = model.fit(lag)
        aic.append(results.aic)
        bic.append(results.bic)
    # Find the lag that has the lowest AIC and BIC
    optimal_lag_aic = np.argmin(aic) + 1
    optimal_lag_bic = np.argmin(bic) + 1
    # Plot the AIC and BIC
    plt.figure(figsize=(12, 6))
    plt.plot(range(1, len(aic) + 1), aic, label='AIC', color='blue')
    plt.plot(range(1, len(bic) + 1), bic, label='BIC', color='red')
    plt.title('AIC and BIC for each lag')
    plt.xlabel('Lag')
    plt.ylabel('Value')
    plt.legend()
    plt.show()

    return optimal_lag_aic, optimal_lag_bic


# Seasonal Differencing for each parameter
# This will be only performed after checking the stationarity of the data to remove the seasonality.
def seasonal_differencing(data, parameter, lag):
    # 1D time series data extraction
    time_series = data[parameter]
    # Seasonal differencing
    seasonal_diff = time_series.diff(periods=lag)
    # Plot the seasonal differencing
    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    plt.plot(data.index, time_series, label='Original')
    plt.title(f'Original {parameter}')
    plt.legend()
    plt.subplot(2, 1, 2)
    plt.plot(data.index, seasonal_diff, label='Seasonal Differencing', color='blue')
    plt.title(f'Seasonal Differencing of {parameter} of lag {lag}')
    plt.legend()
    plt.tight_layout()
    plt.show()

    return seasonal_diff


# ADF test for each parameter to check the stationarity
def adf_test(data,  name=''):
    # Check if the data is constant or not
    if data.std() == 0:
        print(f'The {name} data is constant. No need to check the stationarity.')
        return
    else:
        # ADF test
        adf_stat = adfuller(data, autolag='AIC')
        print(f'ADF Test for {name}')
        print(f'ADF Statistic: %f' % adf_stat[0])
        print(f'p-value: %f' % adf_stat[1])
        print(f'Critical Values:')
        for key, value in adf_stat[4].items():
            print(f'{key}: {value}')
        if adf_stat[1] < 0.05:
            print(f'The {name} data is stationary')
        else:
            print(f'The {name} data is non-stationary')


# Time Series Decomposition for each parameter
def tsd(data, parameter, period):
    # Time Series Decomposition
    decomposition = seasonal_decompose(data[parameter], model='additive', period=period)
    # Plot the decomposition
    plt.figure(figsize=(12, 6))
    plt.subplot(4, 1, 1)
    plt.plot(data.index, data[parameter], label='Original')
    plt.title(f'Original {parameter}')
    plt.legend()
    plt.subplot(4, 1, 2)
    plt.plot(data.index, decomposition.trend, label='Trend', color='blue')
    plt.title(f'Trend of {parameter}')
    plt.legend()
    plt.subplot(4, 1, 3)
    plt.plot(data.index, decomposition.seasonal, label='Seasonal', color='red')
    plt.title(f'Seasonal of {parameter}')
    plt.legend()
    plt.subplot(4, 1, 4)
    plt.plot(data.index, decomposition.resid, label='Residual', color='green')
    plt.title(f'Residual of {parameter}')
    plt.legend()
    plt.tight_layout()
    fig = plt.gcf()
    plt.show()
    # fig.savefig(f'Images/tsd_weather/{period}_Time_Series_Decomposition_{parameter}.png')
    return decomposition


# Check if the data has linear relation (cointegration).
# To do so, engle-granger test will be performed.
# As the combination is larger, this will be calculated concurrently.
def cointegration_test(data):
    # parameter combination without 'weather' as it is categorical
    combination = list(combinations(data.columns, 2))
    combination = [pair for pair in combination if 'weather' not in pair]
    cointegrated_pairs = []
    def test_cointegration(pair):
        var1 = data[pair[0]]
        var2 = data[pair[1]]
        _, p_value, _ = coint(var1, var2)
        if p_value < 0.05:
            return pair
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(tqdm(executor.map(test_cointegration, combination),
                            total=len(combination),
                            desc='Cointegration Test processing...'))
    cointegrated_pairs = [pair for pair in results if pair is not None]
            
    return cointegrated_pairs

# ADF test for each parameter
# app_temp, azimuth, clouds, dewpt, dhi, dni, elev_angle, ghi, precip, rh, slp, snow_rate, solar_rad, temp, uv, vis, weather, wind_dir, wind_gust_spd, wind_spd
for column in weather.columns:
    adf_test(weather[column], column)
# result -> all the parameters are stationary. Therefore, no need to perform the seasonal differencing.

# Time Series Decomposition for each parameter except 'weather' as it is a categorical variable
for column in weather.columns:
    tsd(weather, column, period=24*4*365)
# result -> most of the parameters have seasonality.

# Cointegration Test using Engle-Granger --> No need to perform as the dataset is stationary.
cointegrated_pairs = cointegration_test(weather)
print(cointegrated_pairs)

# # Find the optimal lag for each parameter
# optimal_lags = {}
# for column in weather.columns:
#     optimal_lags[column] = optimal_lag(weather, maxlags=15)
#     print(f'Optimal lag for {column}: AIC - {optimal_lags[column][0]}, BIC - {optimal_lags[column][1]}')
