import pandas as pd
import numpy as np

# Load the dataset
df_led = pd.read_csv('Datasets/preprocessed_led.csv')
df_weather1 = pd.read_csv('Datasets/preprocessed_weather.csv')
df_weather2 = pd.read_csv('Datasets/preprocessed_weather2.csv')

### LED ###
print("The original LED dataset looks like this: \n", df_led)
# Unpivot the LED data
df_led['Start Date Time'] = pd.to_datetime(df_led['Start Date Time'])
df_led.set_index('Start Date Time', inplace=True)
df_led = df_led.reset_index().melt(id_vars=['Start Date Time'], var_name='Loc', value_name='Usage')
print("The unpivoted LED dataset looks like this: \n", df_led)
# Sort the dataset by 'Start Date Time'
df_led.sort_values(by='Start Date Time', inplace=True)
print("The sorted LED dataset looks like this: \n", df_led)
# Only use 2014-10-15 to 2016-10-05
df_led = df_led[(df_led['Start Date Time'] >= '2014-10-15') & (df_led['Start Date Time'] < '2016-10-06')]
print("The LED dataset from 2014-10-15 to 2016-10-05 looks like this: \n", df_led)
print("The number of Nan values in the LED dataset: \n", df_led.isnull().sum())

### Weather ###
print("The original Weather1 dataset looks like this: \n", df_weather1)
print("The original Weather2 dataset looks like this: \n", df_weather2)
df_weather1['Start Date Time'] = pd.to_datetime(df_weather1['Start Date Time'])
df_weather2['Start Date Time'] = pd.to_datetime(df_weather2['Start Date Time'])
# Define the additional date ranges for filtering and dropping
additional_start_date = pd.to_datetime('2014-10-08 00:00:00')
additional_end_date = pd.to_datetime('2014-10-14 23:45:00')
drop_start_date = pd.to_datetime('2016-10-06 00:00:00')
drop_end_date = pd.to_datetime('2016-10-12 23:45:00')
# Filter df_weather1 for the additional range to be appended to df_weather2
additional_data = df_weather1[(df_weather1['Start Date Time'] >= additional_start_date) & (df_weather1['Start Date Time'] <= additional_end_date)]
# Append this additional data to df_weather2
df_weather2 = pd.concat([df_weather2, additional_data], ignore_index=True)
# Now drop the specified range from both df_weather1 and df_weather2
df_weather1 = df_weather1[df_weather1['Start Date Time'] > additional_end_date]
df_weather1 = df_weather1[~((df_weather1['Start Date Time'] >= drop_start_date) & (df_weather1['Start Date Time'] <= drop_end_date))]
print("The filtered Weather1 dataset looks like this: \n", df_weather1)
print("The filtered Weather2 dataset looks like this: \n", df_weather2)

### Check the start and end date of the datasets ###
# LED
print("LED Start Date: ", df_led['Start Date Time'].min())
print("LED End Date: ", df_led['Start Date Time'].max())
# Weather
print("Weather1 Start Date: ", df_weather1['Start Date Time'].min())
print("Weather1 End Date: ", df_weather1['Start Date Time'].max())
print("Weather2 Start Date: ", df_weather2['Start Date Time'].min())
print("Weather2 End Date: ", df_weather2['Start Date Time'].max())

# Save the preprocessed datasets
df_led.to_csv('Datasets/preprocessed_led.csv', index=False)
df_weather1.to_csv('Datasets/preprocessed_weather.csv', index=False)
df_weather2.to_csv('Datasets/preprocessed_weather2.csv', index=False)