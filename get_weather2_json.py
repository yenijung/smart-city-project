import requests
import json

'''
THIS WEATHER DATASET IS ONLY USED FOR WEATHER PREDICTION, NOT FOR DNN
FROM 2010-10-08 00:00:00 TO 2014-10-07 23:45:00
'''

# Get the weather data of las vegas from the API
# Data can only be retrieved for a month at a time
# So the data will be retrieved in a loop for each month
# The data will be saved in a csv file from json format
api_url_10_2010 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2010-10-08:00&end_date=2010-11-01:00&tz=local&key=56cea7b57b634dcf8f3b0af722a81c19"
response = requests.get(api_url_10_2010)
weather_data = response.json()
# Save the data in weather.json file
with open('Datasets/weather2.json', 'w') as f:
    json.dump(weather_data, f, indent=4)
print("successfully saved 2010 October weather data in weather.json file")

# We will loop through the months and save data in weather.json file without overwriting
api_url_11_2010 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2010-11-01:00&end_date=2010-12-01:00&tz=local&key=56cea7b57b634dcf8f3b0af722a81c19"
response = requests.get(api_url_11_2010)
weather_data = response.json()
with open('Datasets/weather2.json', 'a') as f:
    json.dump(weather_data, f, indent=4)
print("successfully saved 2010 November weather data in weather.json file")

api_url_12_2010 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2010-12-01:00&end_date=2011-01-01:00&tz=local&key=56cea7b57b634dcf8f3b0af722a81c19"
response = requests.get(api_url_12_2010)
weather_data = response.json()
with open('Datasets/weather2.json', 'a') as f:
    json.dump(weather_data, f, indent=4)

api_url_01_2011 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2011-01-01:00&end_date=2011-02-01:00&tz=local&key=56cea7b57b634dcf8f3b0af722a81c19"
response = requests.get(api_url_01_2011)
weather_data = response.json()
with open('Datasets/weather2.json', 'a') as f:
    json.dump(weather_data, f, indent=4)

api_url_02_2011 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2011-02-01:00&end_date=2011-03-01:00&tz=local&key=56cea7b57b634dcf8f3b0af722a81c19"
response = requests.get(api_url_02_2011)
weather_data = response.json()
with open('Datasets/weather2.json', 'a') as f:
    json.dump(weather_data, f, indent=4)

api_url_03_2011 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2011-03-01:00&end_date=2011-04-01:00&tz=local&key=56cea7b57b634dcf8f3b0af722a81c19"
response = requests.get(api_url_03_2011)
weather_data = response.json()
with open('Datasets/weather2.json', 'a') as f:
    json.dump(weather_data, f, indent=4)

api_url_04_2011 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2011-04-01:00&end_date=2011-05-01:00&tz=local&key=56cea7b57b634dcf8f3b0af722a81c19"
response = requests.get(api_url_04_2011)
weather_data = response.json()
with open('Datasets/weather2.json', 'a') as f:
    json.dump(weather_data, f, indent=4)

api_url_05_2011 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2011-05-01:00&end_date=2011-06-01:00&tz=local&key=56cea7b57b634dcf8f3b0af722a81c19"
response = requests.get(api_url_05_2011)
weather_data = response.json()
with open('Datasets/weather2.json', 'a') as f:
    json.dump(weather_data, f, indent=4)

api_url_06_2011 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2011-06-01:00&end_date=2011-07-01:00&tz=local&key=56cea7b57b634dcf8f3b0af722a81c19"
response = requests.get(api_url_06_2011)
weather_data = response.json()
with open('Datasets/weather2.json', 'a') as f:
    json.dump(weather_data, f, indent=4)

api_url_07_2011 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2011-07-01:00&end_date=2011-08-01:00&tz=local&key=56cea7b57b634dcf8f3b0af722a81c19"
response = requests.get(api_url_07_2011)
weather_data = response.json()
with open('Datasets/weather2.json', 'a') as f:
    json.dump(weather_data, f, indent=4)

api_url_08_2011 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2011-08-01:00&end_date=2011-09-01:00&tz=local&key=56cea7b57b634dcf8f3b0af722a81c19"
response = requests.get(api_url_08_2011)
weather_data = response.json()
with open('Datasets/weather2.json', 'a') as f:
    json.dump(weather_data, f, indent=4)

api_url_09_2011 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2011-09-01:00&end_date=2011-10-01:00&tz=local&key=56cea7b57b634dcf8f3b0af722a81c19"
response = requests.get(api_url_09_2011)
weather_data = response.json()
with open('Datasets/weather2.json', 'a') as f:
    json.dump(weather_data, f, indent=4)

api_url_10_2011 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2011-10-01:00&end_date=2011-11-01:00&tz=local&key=56cea7b57b634dcf8f3b0af722a81c19"
response = requests.get(api_url_10_2011)
weather_data = response.json()
with open('Datasets/weather2.json', 'a') as f:
    json.dump(weather_data, f, indent=4)

api_url_11_2011 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2011-11-01:00&end_date=2011-12-01:00&tz=local&key=56cea7b57b634dcf8f3b0af722a81c19"
response = requests.get(api_url_11_2011)
weather_data = response.json()
with open('Datasets/weather2.json', 'a') as f:
    json.dump(weather_data, f, indent=4)

api_url_12_2011 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2011-12-01:00&end_date=2012-01-01:00&tz=local&key=56cea7b57b634dcf8f3b0af722a81c19"
response = requests.get(api_url_12_2011)
weather_data = response.json()
with open('Datasets/weather2.json', 'a') as f:
    json.dump(weather_data, f, indent=4)

api_url_01_2012 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2012-01-01:00&end_date=2012-02-01:00&tz=local&key=56cea7b57b634dcf8f3b0af722a81c19"
response = requests.get(api_url_01_2012)
weather_data = response.json()
with open('Datasets/weather2.json', 'a') as f:
    json.dump(weather_data, f, indent=4)

api_url_02_2012 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2012-02-01:00&end_date=2012-03-01:00&tz=local&key=56cea7b57b634dcf8f3b0af722a81c19"
response = requests.get(api_url_02_2012)
weather_data = response.json()
with open('Datasets/weather2.json', 'a') as f:
    json.dump(weather_data, f, indent=4)

api_url_03_2012 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2012-03-01:00&end_date=2012-04-01:00&tz=local&key=56cea7b57b634dcf8f3b0af722a81c19"
response = requests.get(api_url_03_2012)
weather_data = response.json()
with open('Datasets/weather2.json', 'a') as f:
    json.dump(weather_data, f, indent=4)

api_url_04_2012 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2012-04-01:00&end_date=2012-05-01:00&tz=local&key=56cea7b57b634dcf8f3b0af722a81c19"
response = requests.get(api_url_04_2012)
weather_data = response.json()
with open('Datasets/weather2.json', 'a') as f:
    json.dump(weather_data, f, indent=4)

api_url_05_2012 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2012-05-01:00&end_date=2012-06-01:00&tz=local&key=56cea7b57b634dcf8f3b0af722a81c19"
response = requests.get(api_url_05_2012)
weather_data = response.json()
with open('Datasets/weather2.json', 'a') as f:
    json.dump(weather_data, f, indent=4)

api_url_06_2012 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2012-06-01:00&end_date=2012-07-01:00&tz=local&key=56cea7b57b634dcf8f3b0af722a81c19"
response = requests.get(api_url_06_2012)
weather_data = response.json()
with open('Datasets/weather2.json', 'a') as f:
    json.dump(weather_data, f, indent=4)

api_url_07_2012 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2012-07-01:00&end_date=2012-08-01:00&tz=local&key=56cea7b57b634dcf8f3b0af722a81c19"
response = requests.get(api_url_07_2012)
weather_data = response.json()
with open('Datasets/weather2.json', 'a') as f:
    json.dump(weather_data, f, indent=4)

api_url_08_2012 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2012-08-01:00&end_date=2012-09-01:00&tz=local&key=56cea7b57b634dcf8f3b0af722a81c19"
response = requests.get(api_url_08_2012)
weather_data = response.json()
with open('Datasets/weather2.json', 'a') as f:
    json.dump(weather_data, f, indent=4)

api_url_09_2012 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2012-09-01:00&end_date=2012-10-01:00&tz=local&key=56cea7b57b634dcf8f3b0af722a81c19"
response = requests.get(api_url_09_2012)
weather_data = response.json()
with open('Datasets/weather2.json', 'a') as f:
    json.dump(weather_data, f, indent=4)

api_url_10_2012 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2012-10-01:00&end_date=2012-11-01:00&tz=local&key=56cea7b57b634dcf8f3b0af722a81c19"
response = requests.get(api_url_10_2012)
weather_data = response.json()
with open('Datasets/weather2.json', 'a') as f:
    json.dump(weather_data, f, indent=4)

api_url_11_2012 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2012-11-01:00&end_date=2012-12-01:00&tz=local&key=56cea7b57b634dcf8f3b0af722a81c19"
response = requests.get(api_url_11_2012)
weather_data = response.json()
with open('Datasets/weather2.json', 'a') as f:
    json.dump(weather_data, f, indent=4)

api_url_12_2012 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2012-12-01:00&end_date=2013-01-01:00&tz=local&key=56cea7b57b634dcf8f3b0af722a81c19"
response = requests.get(api_url_12_2012)
weather_data = response.json()
with open('Datasets/weather2.json', 'a') as f:
    json.dump(weather_data, f, indent=4)

api_url_01_2013 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2013-01-01:00&end_date=2013-02-01:00&tz=local&key=56cea7b57b634dcf8f3b0af722a81c19"
response = requests.get(api_url_01_2013)
weather_data = response.json()
with open('Datasets/weather2.json', 'a') as f:
    json.dump(weather_data, f, indent=4)

api_url_02_2013 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2013-02-01:00&end_date=2013-03-01:00&tz=local&key=56cea7b57b634dcf8f3b0af722a81c19"
response = requests.get(api_url_02_2013)
weather_data = response.json()
with open('Datasets/weather2.json', 'a') as f:
    json.dump(weather_data, f, indent=4)

api_url_03_2013 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2013-03-01:00&end_date=2013-04-01:00&tz=local&key=56cea7b57b634dcf8f3b0af722a81c19"
response = requests.get(api_url_03_2013)
weather_data = response.json()
with open('Datasets/weather2.json', 'a') as f:
    json.dump(weather_data, f, indent=4)

api_url_04_2013 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2013-04-01:00&end_date=2013-05-01:00&tz=local&key=56cea7b57b634dcf8f3b0af722a81c19"
response = requests.get(api_url_04_2013)
weather_data = response.json()
with open('Datasets/weather2.json', 'a') as f:
    json.dump(weather_data, f, indent=4)

api_url_05_2013 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2013-05-01:00&end_date=2013-06-01:00&tz=local&key=56cea7b57b634dcf8f3b0af722a81c19"
response = requests.get(api_url_05_2013)
weather_data = response.json()
with open('Datasets/weather2.json', 'a') as f:
    json.dump(weather_data, f, indent=4)

api_url_06_2013 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2013-06-01:00&end_date=2013-07-01:00&tz=local&key=56cea7b57b634dcf8f3b0af722a81c19"
response = requests.get(api_url_06_2013)
weather_data = response.json()
with open('Datasets/weather2.json', 'a') as f:
    json.dump(weather_data, f, indent=4)

api_url_07_2013 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2013-07-01:00&end_date=2013-08-01:00&tz=local&key=56cea7b57b634dcf8f3b0af722a81c19"
response = requests.get(api_url_07_2013)
weather_data = response.json()
with open('Datasets/weather2.json', 'a') as f:
    json.dump(weather_data, f, indent=4)

api_url_08_2013 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2013-08-01:00&end_date=2013-09-01:00&tz=local&key=56cea7b57b634dcf8f3b0af722a81c19"
response = requests.get(api_url_08_2013)
weather_data = response.json()
with open('Datasets/weather2.json', 'a') as f:
    json.dump(weather_data, f, indent=4)

api_url_09_2013 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2013-09-01:00&end_date=2013-10-01:00&tz=local&key=56cea7b57b634dcf8f3b0af722a81c19"
response = requests.get(api_url_09_2013)
weather_data = response.json()
with open('Datasets/weather2.json', 'a') as f:
    json.dump(weather_data, f, indent=4)

api_url_10_2013 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2013-10-01:00&end_date=2013-11-01:00&tz=local&key=56cea7b57b634dcf8f3b0af722a81c19"
response = requests.get(api_url_10_2013)
weather_data = response.json()
with open('Datasets/weather2.json', 'a') as f:
    json.dump(weather_data, f, indent=4)

api_url_11_2013 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2013-11-01:00&end_date=2013-12-01:00&tz=local&key=56cea7b57b634dcf8f3b0af722a81c19"
response = requests.get(api_url_11_2013)
weather_data = response.json()
with open('Datasets/weather2.json', 'a') as f:
    json.dump(weather_data, f, indent=4)

api_url_12_2013 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2013-12-01:00&end_date=2014-01-01:00&tz=local&key=56cea7b57b634dcf8f3b0af722a81c19"
response = requests.get(api_url_12_2013)
weather_data = response.json()
with open('Datasets/weather2.json', 'a') as f:
    json.dump(weather_data, f, indent=4)

api_url_01_2014 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2014-01-01:00&end_date=2014-02-01:00&tz=local&key=56cea7b57b634dcf8f3b0af722a81c19"
response = requests.get(api_url_01_2014)
weather_data = response.json()
with open('Datasets/weather2.json', 'a') as f:
    json.dump(weather_data, f, indent=4)

api_url_02_2014 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2014-02-01:00&end_date=2014-03-01:00&tz=local&key=56cea7b57b634dcf8f3b0af722a81c19"
response = requests.get(api_url_02_2014)
weather_data = response.json()
with open('Datasets/weather2.json', 'a') as f:
    json.dump(weather_data, f, indent=4)

api_url_03_2014 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2014-03-01:00&end_date=2014-04-01:00&tz=local&key=56cea7b57b634dcf8f3b0af722a81c19"
response = requests.get(api_url_03_2014)
weather_data = response.json()
with open('Datasets/weather2.json', 'a') as f:
    json.dump(weather_data, f, indent=4)

api_url_04_2014 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2014-04-01:00&end_date=2014-05-01:00&tz=local&key=56cea7b57b634dcf8f3b0af722a81c19"
response = requests.get(api_url_04_2014)
weather_data = response.json()
with open('Datasets/weather2.json', 'a') as f:
    json.dump(weather_data, f, indent=4)

api_url_05_2014 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2014-05-01:00&end_date=2014-06-01:00&tz=local&key=56cea7b57b634dcf8f3b0af722a81c19"
response = requests.get(api_url_05_2014)
weather_data = response.json()
with open('Datasets/weather2.json', 'a') as f:
    json.dump(weather_data, f, indent=4)

api_url_06_2014 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2014-06-01:00&end_date=2014-07-01:00&tz=local&key=56cea7b57b634dcf8f3b0af722a81c19"
response = requests.get(api_url_06_2014)
weather_data = response.json()
with open('Datasets/weather2.json', 'a') as f:
    json.dump(weather_data, f, indent=4)

api_url_07_2014 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2014-07-01:00&end_date=2014-08-01:00&tz=local&key=56cea7b57b634dcf8f3b0af722a81c19"
response = requests.get(api_url_07_2014)
weather_data = response.json()
with open('Datasets/weather2.json', 'a') as f:
    json.dump(weather_data, f, indent=4)

api_url_08_2014 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2014-08-01:00&end_date=2014-09-01:00&tz=local&key=56cea7b57b634dcf8f3b0af722a81c19"
response = requests.get(api_url_08_2014)
weather_data = response.json()
with open('Datasets/weather2.json', 'a') as f:
    json.dump(weather_data, f, indent=4)

api_url_09_2014 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2014-09-01:00&end_date=2014-10-01:00&tz=local&key=56cea7b57b634dcf8f3b0af722a81c19"
response = requests.get(api_url_09_2014)
weather_data = response.json()
with open('Datasets/weather2.json', 'a') as f:
    json.dump(weather_data, f, indent=4)

api_url_10_2014 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2014-10-01:00&end_date=2014-10-08:23&tz=local&key=56cea7b57b634dcf8f3b0af722a81c19"
response = requests.get(api_url_10_2014)
weather_data = response.json()
with open('Datasets/weather2.json', 'a') as f:
    json.dump(weather_data, f, indent=4)
