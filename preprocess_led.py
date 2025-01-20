"""
1. We need to drop the column `Name`, `Account #`, `Customer Code`, `Premise Code`, `Meter ID`, `Service Type`, `Channel Number`,
`Power Flow`, `Unit`, `Interval Length`, `Time Zone`, `Start Date`, `Start Time`, `End Date`, `End Time`, `Time of Use`,
`Read Type`, `Day of the Week`, `Cost` from the dataset.
2. We need to change the `Loc` values into integer values. (Dataset encoding)
3. Time & Date: MM/DD/YYYY HH:MM:SS AM/PM (`Start Date Time`, `End Date Time`)
    -> This should be unified with the format of the 'timestamp_utc' in the weather dataset.
       Also, this should be combined into one column as it has been measured once in every 15 minutes.
       Therefore, `End Date Time` can be dropped as well.
4. The starting time/date and the ending time/date of the dataset should be matched with the weather dataset.
  -> Start date/time: 08/10/2014 00:00:00
     End date/time: 12/10/2016 23:45:00
     As there is no exceeded time/date in this dataset, no need to be trimmed this dataset further.
Warning: The dataset should not be normalized before the data splitting with data leakage reason.
         Therefore, after the data splitting, fit method will be called only to the training dataset.
"""

import pandas as pd

# read the csv file
df = pd.read_csv('Datasets/led_lighting.csv')

# drop the columns (1)
df = df.drop(columns=['Name', 'Account #', 'Customer Code', 'Premise Code', 'Meter ID', 'Service Type', 'Channel Number',
                      'Power Flow', 'Unit', 'Interval Length', 'Time Zone', 'Start Date', 'Start Time', 'End Date',
                      'End Time', 'Time of Use', 'Read Type', 'Day of the Week', 'Cost', 'End Date Time', 'Hour of the Day'])

# change the `Loc` values into integer values (2)
def map_loc_to_int(dataset):
    unique_loc = dataset['Loc'].unique()
    loc_mapping = {loc: i for i, loc in enumerate(unique_loc, start=1)}
    dataset['Loc'] = dataset['Loc'].map(loc_mapping)
    return dataset

df = map_loc_to_int(df)

# We need to change the `Start Date Time` format into 24-hour format (3)
# Also we need to change the `Start Date Time` format into DD/MM/YYYY HH:MM:SS AM/PM
from datetime import datetime

def convert_timeline(timeline):
    dt = datetime.strptime(timeline, '%m/%d/%Y %I:%M:%S %p')
    changed_timeline = dt.strftime('%d/%m/%Y %H:%M:%S')
    return changed_timeline

df['Start Date Time'] = df['Start Date Time'].apply(convert_timeline)
#print(df)

# save the preprocessed dataset
df.to_csv('Datasets/preprocessed_led.csv', index=False)

