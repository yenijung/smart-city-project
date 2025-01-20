'''
1. We need to drop the column 'revision_status', 'timestamp_local', 'ts', 'pod'
2. Time & Date : YYYY-MM-DDTHH:MM:SS (`timestamp_utc`)
  -> This should be unified with the format of the 'Start Date Time' in the led_lighting dataset.
     Therefore, YYYY-MM-DDTHH:MM:SS format should be changed into DD/MM/YYYY HH:MM:SS AM/PM.
     Also, the 'timestamp_utc' column should be renamed as 'Start Date Time'.
3. 'weather' column should be sorted out what to use for the analysis.
  -> Check the api description to see what kind of values are included in 'description' sub-column.
     If it is not necessary, it can be dropped.
4. The starting time/date and the ending time/date of the dataset should be matched with the led_lighting dataset.
  -> Start date/time: 08/10/2014 00:00:00
     End date/time: 31/10/2016 23:45:00
     As there is exceeded time/date in this dataset, it should be dropped.
'''
import numpy as np
import pandas as pd
from datetime import datetime
from matplotlib import pyplot as plt
import seaborn as sns

# read the csv file
df1 = pd.read_csv('Datasets/weather.csv')
df2 = pd.read_csv('Datasets/weather2.csv')
# the weather2 dataset is collected from 2010-10-08 to 2014-10-07

# drop the columns-1 (1)
df1 = df1.drop(columns=['revision_status', 'timestamp_utc', 'ts', 'weather', 'slp', 'dni', 'dhi', 'pod'])
df2 = df2.drop(columns=['revision_status', 'timestamp_utc', 'ts', 'weather', 'slp', 'dni', 'dhi', 'pod'])

# rename the column (2)
df1 = df1.rename(columns={'timestamp_local': 'Start Date Time'})
df2 = df2.rename(columns={'timestamp_local': 'Start Date Time'})

# match the starting time/date and the ending time/date of the dataset with the led_lighting dataset (4)
df1['Start Date Time'] = pd.to_datetime(df1['Start Date Time'], format='%Y-%m-%dT%H:%M:%S')
df2['Start Date Time'] = pd.to_datetime(df2['Start Date Time'], format='%Y-%m-%dT%H:%M:%S')
start_date = pd.to_datetime('2014-10-08T00:00:00', format='%Y-%m-%dT%H:%M:%S')
end_date = pd.to_datetime('2016-10-12T23:45:00', format='%Y-%m-%dT%H:%M:%S')
df1.drop(df1[(df1['Start Date Time'] < start_date) | (df1['Start Date Time'] > end_date)].index, inplace=True)

# Combine the two datasets
combined_df = pd.concat([df2, df1], ignore_index=True)
combined_df = combined_df.sort_values(by='Start Date Time')
combined_df['Start Date Time'] = pd.to_datetime(combined_df['Start Date Time'], format='%Y-%m-%d %H:%M:%S')
combined_df.set_index('Start Date Time', inplace=True)

# Check if there's any column that is fully filled with NaN or 0
print("Total number of rows: ", len(combined_df))
print("Columns with NaN or 0 values: ")
print(combined_df.isnull().sum())
print("Columns with 0 values: ")
print(combined_df.isin([0]).sum())
print("Columns with NaN values: ")
print(combined_df.isin([np.nan]).sum())
#### Check if there is any outlier in the dataset ####
combined_df = combined_df.drop(columns=['snow_rate'])     # as it is filled with only 0 values
# Check the correlation between the columns
numerical_df = combined_df.select_dtypes(include=[np.number])
plt.figure(figsize=(13, 13))
plt.title('Original correlations between the columns')
sns.heatmap(numerical_df.corr(), annot=True, cmap='coolwarm')
plt.show()
# app_temp and temp are highly correlated in the value of 0.99. Therefore, app_temp will be dropped.
# This is because temp is more subjectively measured than app_temp.
combined_df.drop(columns=['app_temp'], inplace=True)
# ghi and solar_rad are highly correlated in the value of 0.97. Therefore, solar_rad will be dropped.
# This is because solar_rad is a total solar energy received by the earth whereas ghi is a total solar energy received by a horizontal surface.
combined_df.drop(columns=['solar_rad'], inplace=True)
# wind_spd and wind_gust_spd are highly correlated in the value of 0.8. Therefore, wind_gust_spd will be dropped.
# This is because wind_gust_spd is a maximum wind speed whereas wind_spd is an average wind speed.
combined_df.drop(columns=['wind_gust_spd'], inplace=True)
# ghi and uv are highly correlated in the value of 0.94. Therefore, uv will be dropped.
# This is because ghi is a total solar energy received by a horizontal surface whereas uv is a UV index.
combined_df.drop(columns=['uv'], inplace=True)
# ghi and elev_angle are highly correlated in the value of 0.87. Therefore, elev_angle will be dropped.
# This is because ghi is a total solar energy received by a horizontal surface whereas elev_angle is an elevation angle of the sun, which is not necessary.
combined_df.drop(columns=['elev_angle'], inplace=True)
# Check the correlation between the columns again
plt.figure(figsize=(13, 13))
numerical_df2 = combined_df.select_dtypes(include=[np.number])
plt.title('Correlations between the columns after dropping columns')
sns.heatmap(numerical_df2.corr(), annot=True, cmap='coolwarm')
plt.show()

# Fill NaN values with time series interpolation as the dataset is time series data
combined_df['dewpt'] = combined_df['dewpt'].interpolate(method='time')
# Check again if there's any column that is fully filled with NaN or 0
print("Total number of rows: ", len(combined_df))
print("Columns with NaN or 0 values: ")
print(combined_df.isnull().sum())
print("Columns with 0 values: ")
print(combined_df.isin([0]).sum())
print("Columns with NaN values: ")
print(combined_df.isin([np.nan]).sum())

print(combined_df)
# Save the preprocessed dataset separately as well
df1 = combined_df.loc[:'2014-10-08 00:00:00']
df2 = combined_df.loc['2014-10-08 00:00:00':]
df1_reset = df1.reset_index()
df2_reset = df2.reset_index()
print(df1)
print(df2)
df1.to_csv('Datasets/preprocessed_weather2.csv')
df2.to_csv('Datasets/preprocessed_weather.csv')
