"""
Now we will preprocess the data values for the LED dataset.
1. 'Start Date Time' should be converted into a datetime object.
2. Data splitting (for individual AI model)
    -> First, the dataset should be split into two parts: training and testing.
    -> Then, the training dataset should be split into two parts: training and validation.
    -> Training : Validation : Testing = 70 : 15 : 15
    -> Criteria: As 'Weather' dataset will be split by 'Start Date Time'
       this dataset should be split by 'Start Date Time' as well.
"""

# Convert 'Start Date Time' into a datetime object
import pandas as pd
from datetime import datetime
df = pd.read_csv('Datasets/preprocessed_led.csv')
df['Start Date Time'] = pd.to_datetime(df['Start Date Time'], dayfirst=True, errors='coerce')
print(df['Start Date Time'].head())
# result: 'Start Date Time' -> datatype: datetime64[ns]

# Data splitting
# First, reorder the dataset by 'Start Date Time'.
df_sorted = df.sort_values(by='Start Date Time')
# Pivot the LED data
df_sorted = df_sorted.pivot_table(values='Usage', index=df_sorted['Start Date Time'], columns='Loc')
print(df_sorted.head(10))

def check_duplicates(df):
    duplicates = df.index.duplicated(keep=False)
    if duplicates.any():
        print('There are duplicated values in the dataset.')
        print(df[duplicates])
    else:
        print('There are no duplicated values in the dataset.')
    return duplicates

def handle_duplicates(df):
    # Check for all occurrences of duplicates
    duplicates = df.index.duplicated(keep=False)
    if not duplicates.any():
        print("No duplicates to handle.")
        return df
    averaged = df.groupby('Start Date Time', as_index=False).mean()
    averaged.sort_values(by='Start Date Time', inplace=True)
    return averaged

duplicates = check_duplicates(df_sorted)
df_final = handle_duplicates(df_sorted)
duplicates2 = check_duplicates(df_final)

# Split the dataset into training, validation, and testing datasets
# Training : Validation : Testing =  60 : 20 : 20
# Training : Validation 1 : Validation 2 : Testing = 60 : 10 : 10 : 20
n = len(df_sorted)
train_df = int(n * 0.6)
val_df = train_df + int(n * 0.2)

train = df_sorted.iloc[:train_df]
validation = df_sorted.iloc[train_df:val_df]
test = df_sorted.iloc[val_df:]

print("Train:", train)
print("Validation1:", validation)
print("Test:", test)

# Reset the index for the split datasets and make the value into 'Usage'
def reset_index(df):
    df.reset_index(inplace=True)
    df = df.melt(id_vars=['Start Date Time'], var_name='Loc', value_name='Usage')
    df.sort_values(by='Start Date Time', inplace=True)
    return df

train = reset_index(train)
validation = reset_index(validation)
test = reset_index(test)

print("Train:", train)
print("Validation:", validation)
print("Test:", test)

# Save the split datasets
train.to_csv('Datasets/led_train.csv', index=False)
validation.to_csv('Datasets/led_validation.csv', index=False)
test.to_csv('Datasets/led_test.csv', index=False)
print('Successfully saved the split datasets.')