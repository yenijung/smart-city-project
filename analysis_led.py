"""
The analysis of this data is not very necessary as lstm doesn't have lots of limitations.
However, it will be further important to know the feature of the dataset
for the analysis with weather data, 2 analyses will be performed.
1. Stationarity check
2. Seasonality check
"""

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller

# Load the prepared led data
led = pd.read_csv('Datasets/preprocessed_led.csv', index_col=0, parse_dates=True)
# Make the index into normal column
led.reset_index(inplace=True)
# Convert the 'Start Date Time' column into datetime type from object type
led['Start Date Time'] = pd.to_datetime(led['Start Date Time'], format='%d/%m/%Y %H:%M:%S')
# Set the 'Start Date Time' column as the index
led.set_index('Start Date Time', inplace=True)
# Pivot the dataset to have the locations as columns
led = led.pivot_table(values='Usage', index=led.index, columns='Loc')
print(led.isnull().sum())

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
            print(f'Location {name} is stationary')
        else:
            print(f'Location {name} data is non-stationary')


# Time series decomposition for each location
def tsd(data, location, period):
    # Time Series Decomposition
    decomposition = seasonal_decompose(data[location], model='additive', period=period)
    # Plot the decomposition
    plt.figure(figsize=(12, 6))
    plt.subplot(4, 1, 1)
    plt.plot(data.index, data[location], label='Original')
    plt.title(f'Original usage in Location {location}')
    plt.legend()
    plt.subplot(4, 1, 2)
    plt.plot(data.index, decomposition.trend, label='Trend', color='blue')
    plt.title(f'Trend of the usage in Location {location}')
    plt.legend()
    plt.subplot(4, 1, 3)
    plt.plot(data.index, decomposition.seasonal, label='Seasonal', color='red')
    plt.title(f'Seasonal of the usage in Location {location}')
    plt.legend()
    plt.subplot(4, 1, 4)
    plt.plot(data.index, decomposition.resid, label='Residual', color='green')
    plt.title(f'Residual of the usage in Location {location}')
    plt.legend()
    plt.tight_layout()
    fig = plt.gcf()
    plt.show()
    # fig.savefig(f'Images/tsd_led/{period}_Time_Series_Decomposition_Loc{location}.png')
    return decomposition


def plot_daily_usage(data, date):
    daily_data = data.loc[date]
    plt.figure(figsize=(12, 6))
    for loc in daily_data.columns:
        plt.plot(daily_data.index, daily_data[loc], label=f'Location {loc}')
    plt.title(f'LED Usage on {date}')
    plt.xlabel('Time')
    plt.ylabel('Usage')
    plt.legend()
    plt.tight_layout()
    fig = plt.gcf()
    plt.show()
    fig.savefig(f'Images/daily_usage_led/{date}_daily_usage.png')


def iqr_outlier_removal(data, column):
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    data[column] = np.where((data[column] < lower_bound) | (data[column] > upper_bound),
                            data[column].median(), data[column])

for col in led.columns:
    iqr_outlier_removal(led, col)

def daily_usage(data):
    daily_data = data.resample('D').sum()
    plt.figure(figsize=(12, 8))
    for loc in daily_data.columns:
        plt.plot(daily_data.index, daily_data[loc], label=f'Location {loc}')
    plt.title('Daily Sum Energy Usage per Location')
    plt.xlabel('Date')
    plt.ylabel('Energy Usage')
    plt.legend(loc='upper right', bbox_to_anchor=(1.2, 1))
    plt.tight_layout()
    fig = plt.gcf()
    plt.show()
    fig.savefig('Images/daily_sum_led.png')


def trends(data):
    plt.figure(figsize=(12, 8))
    for loc in data.columns:
        decomposed = seasonal_decompose(data[loc].dropna(), model='additive', period=4*24*30)
        trend = decomposed.trend
        plt.plot(data.index, trend, label=f'Location {loc}')
    plt.title('Trend of Energy Usage per Location')
    plt.xlabel('Date')
    plt.ylabel('Energy Usage')
    # plt.tight_layout()
    fig = plt.gcf()
    plt.legend(loc='upper right', bbox_to_anchor=(1.2, 1))
    plt.show()
    fig.savefig('Images/trends_led.png')


# # Perform the ADF test for each location
# for loc in led.columns:
#     adf_test(led[loc], name=loc)
#     print('----------------------------------------')
#
# Perform the time series decomposition for each location
# for loc in led.columns:
    # tsd(led, loc,  4*24)    # daily
    # tsd(led, loc,  4*7*24)    # weekly
    # tsd(led, loc,  4*30*24)    # monthly
    # tsd(led, loc,  4*365*24)    # seasonal

# # Plot the daily usage of the LED - the date is randomly chosen
# plot_daily_usage(led, '2014-12-19')
# plot_daily_usage(led, '2015-05-21')
# plot_daily_usage(led, '2016-07-08')

daily_usage(led)
trends(led)
