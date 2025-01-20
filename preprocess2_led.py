##### Preprocess 2 of led dataset #####

import numpy as np
import pandas as pd

# Load datasets
df_led = pd.read_csv('Datasets/preprocessed_led.csv')
df_weather = pd.read_csv('Datasets/preprocessed_weather.csv')

# Convert 'Start Date Time' to datetime
df_led['Start Date Time'] = pd.to_datetime(df_led['Start Date Time'], dayfirst=True, errors='coerce')
df_weather['Start Date Time'] = pd.to_datetime(df_weather['Start Date Time'], format='%Y-%m-%d %H:%M:%S')

# Before pivoting, extract date for later use in checking 48 data points per day per location
df_led['date'] = df_led['Start Date Time'].dt.date

# Set 'Start Date Time' as index
df_led.set_index('Start Date Time', inplace=True)
df_weather.set_index('Start Date Time', inplace=True)

# Pivot the LED data
df_led_pivoted = df_led.pivot_table(values='Usage', index=df_led.index, columns='Loc')
df_led.sort_index(inplace=True)

# Print the total length of each dataset
print("LED Dataset Length:", len(df_led_pivoted))
print("Weather Dataset Length:", len(df_weather))

# Check if the total lengths are not equal and print the first and last 'Start Date Time'
if len(df_led_pivoted) != len(df_weather):
    print("LED First Date:", df_led_pivoted.index[0])
    print("LED Last Date:", df_led_pivoted.index[-1])
    print("Weather First Date:", df_weather.index[0])
    print("Weather Last Date:", df_weather.index[-1])

# Total should be 24*4*736 = 70656
# LED: 70647, Weather: 70656
# Check every day in every loc has 48 data points for LED dataset
# As we extracted 'date' before, no need to do it again. Directly melt the pivoted DataFrame
def check_96_data_points_per_day(df_led_pivoted):
    df_long = df_led_pivoted.reset_index().melt(id_vars=['Start Date Time'], var_name='Loc', value_name='Usage')
    df_long['date'] = df_long['Start Date Time'].dt.date  # Extract date again as we reset the index
    data_points_per_day_loc = df_long.groupby(['date', 'Loc']).size().reset_index(name='count')
    data_points_per_day_loc['has_all_96'] = data_points_per_day_loc['count'] == 96
    missing_96 = data_points_per_day_loc[data_points_per_day_loc['has_all_96'] == False]

    if missing_96.empty:
        print('All locations have 96 data points per day.')
        return pd.DataFrame()
    else:
        print('Some locations do not have 96 data points per day:')
        return missing_96

missing_96 = check_96_data_points_per_day(df_led_pivoted)
if not missing_96.empty:
    print(missing_96)

# 2015-03-08 02:00:00 to 2015-03-08 02:45:00 is missing for every location
# 2016-03-13 02:00:00 to 2016-03-13 02:45:00 is missing for every location
def insert_missing_timestamps(df, start, end, freq='15T'):
    missing_times = pd.date_range(start=start, end=end, freq=freq)
    for time in missing_times:
        if time not in df.index:
            df.loc[time] = np.nan
    df.sort_index(inplace=True)

insert_missing_timestamps(df_led_pivoted, '2015-03-08 01:45:00', '2015-03-08 02:45:00')
insert_missing_timestamps(df_led_pivoted, '2016-03-13 01:45:00', '2016-03-13 02:45:00')
# Interpolate the missing values
df_led_pivoted.interpolate(method='time', inplace=True)

# Check again
print("LED Dataset Length after Interpolation:", len(df_led_pivoted))
missing_96 = check_96_data_points_per_day(df_led_pivoted)
if missing_96 is not None and not missing_96.empty:
    print("After interpolation, some locations do not have 96 data points per day:")
    print(missing_96)
else:
    print("All locations have 96 data points per day after interpolation.")

# Save the preprocessed LED dataset
df_led_pivoted.to_csv('Datasets/preprocessed_led.csv')
print("Successfully overwrite the preprocessed LED dataset.")
