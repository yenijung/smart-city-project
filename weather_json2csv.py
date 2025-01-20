'''
weather.json file is the file that contains multiple json objects.
To convert this into csv file without error, we need to delete the repeated keys in the json objects.
repeated keys are: "city_id": "5506956", "city_name": "Las Vegas", "country_code": "US"
And we need to change the json structure to make sure that there is only one json object in the file.
'''

import json
import csv

# read the json file
with open('Datasets/weather2.json') as f:
    data = json.load(f)

# delete the repeated keys
for i in range(len(data)):
    del data[i]['city_id']
    del data[i]['city_name']
    del data[i]['country_code']

# write the data to a new json file with the same json indentation structure as the original file
with open('Datasets/weather2_new.json', 'w') as f:
    json.dump(data, f, indent=4)

# The column names are; "app_temp", "azimuth", "clouds", "dewpt", "dhi", "dni", "elev_angle", "ghi", "pod",
# "precip_rate", "pres", "revision_status", "rh", "slp", "snow_rate", "solar_rad", "temp", "timestamp_local",
# "timestamp_utc", "ts", "uv", "vis", "weather" : "code", "description", "icon", "wind_dir", "wind_gust_spd",
# "wind_spd" We would like to extract the values of these columns from the json file and write them to a csv file.

import pandas as pd

with open('Datasets/weather2_new.json') as f:
    data_list = json.load(f)

all_data = []
for item in data_list:
    all_data.extend(item['data'])

df = pd.DataFrame(all_data)

columns = ["app_temp", "azimuth", "clouds", "dewpt", "dhi", "dni", "elev_angle", "ghi", "pod", "precip_rate", "pres", "revision_status", "rh", "slp", "snow_rate", "solar_rad", "temp", "timestamp_local", "timestamp_utc", "ts", "uv", "vis", "weather_code", "weather_description", "weather_icon", "wind_dir", "wind_gust_spd", "wind_spd"]

df.to_csv('Datasets/weather2.csv', index=False, header=True)

# TODO = '''The csv file is successfully created but the column names are not recognized by pycharm.
'''It seems like there is no problem with the file but if it turns out problematically in the future,
this needs to be checked again.'''