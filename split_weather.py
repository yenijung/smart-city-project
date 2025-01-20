"""
Now we will preprocess the data values for the Weather dataset.
1. 'Start Date Time' should be converted into a datetime object.
2. Check if there is any seasonal pattern in the dataset.
    -> If there is any seasonal pattern, we will adopt SARIMA model.
    -> If there is no seasonal pattern, we will adopt LSTM or ARIMA model.
3. Data splitting (for individual AI model)
    -> First, the dataset should be split into two parts: training and testing.
    -> Then, the training dataset should be split into two parts: training and validation.
    -> Training : Validation : Testing = 70 : 15 : 15
    -> Criteria: 'Start Date Time'
"""

# Convert 'Start Date Time' into a datetime object
import pandas as pd
from datetime import datetime
df = pd.read_csv('Datasets/preprocessed_weather.csv')
df2 = pd.read_csv('Datasets/preprocessed_weather2.csv')
df['Start Date Time'] = pd.to_datetime(df['Start Date Time'], errors='coerce')
df2['Start Date Time'] = pd.to_datetime(df2['Start Date Time'], errors='coerce')
#print(df['Start Date Time'].head())

# Count total number of rows
total_n = len(df)
#print(total_n) -> 70656
# As the date range is 2014-10-08 to 2016-10-12, the period will be 70656 / 3 = 23552

# Data splitting
# First, reorder the dataset by 'Start Date Time'.
df = df.sort_values(by='Start Date Time')
df2 = df2.sort_values(by='Start Date Time')
#print(df_sorted.head(10))

##### DUPLICATE CHECK #####
def check_duplicates(df):
    duplicates = df['Start Date Time'].duplicated(keep=False)
    if duplicates.any():
        print('There are duplicated values in the dataset.')
        print(df[duplicates])
    else:
        print('There are no duplicated values in the dataset.')
    return duplicates

def handle_duplicates(df):
    # Check for all occurrences of duplicates
    duplicates = df['Start Date Time'].duplicated(keep=False)
    if not duplicates.any():
        print("No duplicates to handle.")
        return df
    averaged = df.groupby('Start Date Time', as_index=False).mean()
    return averaged

duplicates = check_duplicates(df)
df_final = handle_duplicates(df)
duplicates2 = check_duplicates(df_final)

duplicates3 = check_duplicates(df2)
df2_final = handle_duplicates(df2)
duplicates4 = check_duplicates(df2_final)

##### OMISSION OF START DATE TIME CHECK #####
# Convert 'Start Date Time' into a datetime object
df_final['Start Date Time'] = pd.to_datetime(df_final['Start Date Time'])
df_final.set_index('Start Date Time', inplace=True)
# Resample the DataFrame to a 15-minute frequency, introducing NaNs for missing times
df_resample = df_final.resample('15min').asfreq()
# Group by the date and count the number of data points per day
daily_counts = df_resample.groupby(df_resample.index.date).size()
# Identify any days that do not have 96 data points
days_with_gaps = daily_counts[daily_counts != 96]

if not days_with_gaps.empty:
    print("Days with missing data points identified:")
    print(days_with_gaps)
    # Interpolate missing values for days with gaps
    df_interpolated = df_resample.groupby(df_resample.index.date).apply(lambda x: x.interpolate(method='time'))
    # Drop the groupby level to return the DataFrame to its original shape
    df_interpolated.reset_index(level=0, drop=True, inplace=True)
else:
    print("All days have 96 data points.")
    df_interpolated = df_resample

df2_final['Start Date Time'] = pd.to_datetime(df2_final['Start Date Time'])
df2_final.set_index('Start Date Time', inplace=True)
df2_resample = df2_final.resample('15min').asfreq()
daily_counts2 = df2_resample.groupby(df2_resample.index.date).size()
days_with_gaps2 = daily_counts2[daily_counts2 != 96]

if not days_with_gaps2.empty:
    print("Days with missing data points identified:")
    print(days_with_gaps2)
    df2_interpolated = df2_resample.groupby(df2_resample.index.date).apply(lambda x: x.interpolate(method='time'))
    df2_interpolated.reset_index(level=0, drop=True, inplace=True)

else:
    print("All days have 96 data points.")
    df2_interpolated = df2_resample

##### DATA SPLITTING #####
# Split the dataset into training, validation, and testing datasets
# Training : Validation : Testing =  60 : 20 : 20
n = len(df_interpolated)
train_df = int(n * 0.6)
val_df = train_df + int(n * 0.2)

train = df_interpolated.iloc[:train_df]
validation = df_interpolated.iloc[train_df:val_df]
test = df_interpolated.iloc[val_df:]
df_combined = pd.concat([df2_interpolated, train])

#print('Train:', len(train), 'Validation:', len(validation), 'Test:', len(test))
# result = Train: 49459, Validation: 10598, Test: 10599
print("Train:", train)
print("Validation:", validation)
print("Test:", test)
# print("Combined:", df_combined)

# Unindex the 'Start Date Time' column to make the datasets have the datetime column
train.reset_index(inplace=True)
validation.reset_index(inplace=True)
test.reset_index(inplace=True)
# df_combined.reset_index(inplace=True)

print("Train:", train)
print("Validation1:", validation)
print("Test:", test)
# print("Combined:", df_combined)

# Save the split datasets
train.to_csv('Datasets/weather_train.csv', index=False)
validation.to_csv('Datasets/weather_validation1.csv', index=False)
test.to_csv('Datasets/weather_test.csv', index=False)
print('Successfully saved the split datasets.')

df2_interpolated.reset_index(inplace=True)
df_combined.reset_index(inplace=True)

# Save dataset 2
df2_interpolated.to_csv('Datasets/preprocessed_weather2.csv', index=False)

# Save dataset for weather lstm train - combine the two datasets
df_combined.to_csv('Datasets/preprocessed_weather_combined.csv', index=False)
