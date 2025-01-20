import requests
import json

# Get the weather data of las vegas from the API
# Data can only be retrieved for a month at a time
# So the data will be retrieved in a loop for each month
# The data will be saved in a csv file from json format
api_url_10_2014 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2014-10-08:00&end_date=2014-11-01:00&tz=utc&key=d8398d8f101c45a5bd9847c85dfa8eb2"
response = requests.get(api_url_10_2014)
weather_data = response.json()
"""
print("successfully retrieved weather data")
# We want to print the json data with indentation
print(json.dumps(weather_data, indent=4))
"""
# Save the data in weather.json file
with open('Datasets/weather.json', 'w') as f:
    json.dump(weather_data, f, indent=4)
print("successfully saved 2014 October weather data in weather.json file")

# We will loop through the months and save data in weather.json file without overwriting
api_url_11_2014 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2014-11-01:00&end_date=2014-12-01:00&tz=utc&key=d8398d8f101c45a5bd9847c85dfa8eb2"
response = requests.get(api_url_11_2014)
weather_data = response.json()
with open('Datasets/weather.json', 'a') as f:
    json.dump(weather_data, f, indent=4)
print("successfully saved 2014 November weather data in weather.json file")

api_url_12_2014 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2014-12-01:00&end_date=2015-01-01:00&tz=utc&key=d8398d8f101c45a5bd9847c85dfa8eb2"
response = requests.get(api_url_12_2014)
weather_data = response.json()
with open('Datasets/weather.json', 'a') as f:
    json.dump(weather_data, f, indent=4)
print("successfully saved 2014 December weather data in weather.json file")

api_url_01_2015 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2015-01-01:00&end_date=2015-02-01:00&tz=utc&key=d8398d8f101c45a5bd9847c85dfa8eb2"
response = requests.get(api_url_01_2015)
weather_data = response.json()
with open('Datasets/weather.json', 'a') as f:
    json.dump(weather_data, f, indent=4)
print("successfully saved 2015 January weather data in weather.json file")

api_url_02_2015 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2015-02-01:00&end_date=2015-03-01:00&tz=utc&key=d8398d8f101c45a5bd9847c85dfa8eb2"
response = requests.get(api_url_02_2015)
weather_data = response.json()
with open('Datasets/weather.json', 'a') as f:
    json.dump(weather_data, f, indent=4)
print("successfully saved 2015 February weather data in weather.json file")

api_url_03_2015 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2015-03-01:00&end_date=2015-04-01:00&tz=utc&key=d8398d8f101c45a5bd9847c85dfa8eb2"
response = requests.get(api_url_03_2015)
weather_data = response.json()
with open('Datasets/weather.json', 'a') as f:
    json.dump(weather_data, f, indent=4)
print("successfully saved 2015 March weather data in weather.json file")

api_url_04_2015 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2015-04-01:00&end_date=2015-05-01:00&tz=utc&key=d8398d8f101c45a5bd9847c85dfa8eb2"
response = requests.get(api_url_04_2015)
weather_data = response.json()
with open('Datasets/weather.json', 'a') as f:
    json.dump(weather_data, f, indent=4)
print("successfully saved 2015 April weather data in weather.json file")

api_url_05_2015 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2015-05-01:00&end_date=2015-06-01:00&tz=utc&key=d8398d8f101c45a5bd9847c85dfa8eb2"
response = requests.get(api_url_05_2015)
weather_data = response.json()
with open('Datasets/weather.json', 'a') as f:
    json.dump(weather_data, f, indent=4)
print("successfully saved 2015 May weather data in weather.json file")

api_url_06_2015 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2015-06-01:00&end_date=2015-07-01:00&tz=utc&key=d8398d8f101c45a5bd9847c85dfa8eb2"
response = requests.get(api_url_06_2015)
weather_data = response.json()
with open('Datasets/weather.json', 'a') as f:
    json.dump(weather_data, f, indent=4)
print("successfully saved 2015 June weather data in weather.json file")

api_url_07_2015 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2015-07-01:00&end_date=2015-08-01:00&tz=utc&key=d8398d8f101c45a5bd9847c85dfa8eb2"
response = requests.get(api_url_07_2015)
weather_data = response.json()
with open('Datasets/weather.json', 'a') as f:
    json.dump(weather_data, f, indent=4)
print("successfully saved 2015 July weather data in weather.json file")

api_url_08_2015 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2015-08-01:00&end_date=2015-09-01:00&tz=utc&key=d8398d8f101c45a5bd9847c85dfa8eb2"
response = requests.get(api_url_08_2015)
weather_data = response.json()
with open('Datasets/weather.json', 'a') as f:
    json.dump(weather_data, f, indent=4)
print("successfully saved 2015 August weather data in weather.json file")

api_url_09_2015 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2015-09-01:00&end_date=2015-10-01:00&tz=utc&key=d8398d8f101c45a5bd9847c85dfa8eb2"
response = requests.get(api_url_09_2015)
weather_data = response.json()
with open('Datasets/weather.json', 'a') as f:
    json.dump(weather_data, f, indent=4)
print("successfully saved 2015 September weather data in weather.json file")

api_url_10_2015 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2015-10-01:00&end_date=2015-11-01:00&tz=utc&key=d8398d8f101c45a5bd9847c85dfa8eb2"
response = requests.get(api_url_10_2015)
weather_data = response.json()
with open('Datasets/weather.json', 'a') as f:
    json.dump(weather_data, f, indent=4)
print("successfully saved 2015 October weather data in weather.json file")

api_url_11_2015 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2015-11-01:00&end_date=2015-12-01:00&tz=utc&key=d8398d8f101c45a5bd9847c85dfa8eb2"
response = requests.get(api_url_11_2015)
weather_data = response.json()
with open('Datasets/weather.json', 'a') as f:
    json.dump(weather_data, f, indent=4)
print("successfully saved 2015 November weather data in weather.json file")

api_url_12_2015 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2015-12-01:00&end_date=2016-01-01:00&tz=utc&key=d8398d8f101c45a5bd9847c85dfa8eb2"
response = requests.get(api_url_12_2015)
weather_data = response.json()
with open('Datasets/weather.json', 'a') as f:
    json.dump(weather_data, f, indent=4)
print("successfully saved 2015 December weather data in weather.json file")

api_url_01_2016 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2016-01-01:00&end_date=2016-02-01:00&tz=utc&key=d8398d8f101c45a5bd9847c85dfa8eb2"
response = requests.get(api_url_01_2016)
weather_data = response.json()
with open('Datasets/weather.json', 'a') as f:
    json.dump(weather_data, f, indent=4)
print("successfully saved 2016 January weather data in weather.json file")

api_url_02_2016 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2016-02-01:00&end_date=2016-03-01:00&tz=utc&key=d8398d8f101c45a5bd9847c85dfa8eb2"
response = requests.get(api_url_02_2016)
weather_data = response.json()
with open('Datasets/weather.json', 'a') as f:
    json.dump(weather_data, f, indent=4)
print("successfully saved 2016 February weather data in weather.json file")

api_url_03_2016 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2016-03-01:00&end_date=2016-04-01:00&tz=utc&key=d8398d8f101c45a5bd9847c85dfa8eb2"
response = requests.get(api_url_03_2016)
weather_data = response.json()
with open('Datasets/weather.json', 'a') as f:
    json.dump(weather_data, f, indent=4)
print("successfully saved 2016 March weather data in weather.json file")

api_url_04_2016 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2016-04-01:00&end_date=2016-05-01:00&tz=utc&key=d8398d8f101c45a5bd9847c85dfa8eb2"
response = requests.get(api_url_04_2016)
weather_data = response.json()
with open('Datasets/weather.json', 'a') as f:
    json.dump(weather_data, f, indent=4)
print("successfully saved 2016 April weather data in weather.json file")

api_url_05_2016 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2016-05-01:00&end_date=2016-06-01:00&tz=utc&key=d8398d8f101c45a5bd9847c85dfa8eb2"
response = requests.get(api_url_05_2016)
weather_data = response.json()
with open('Datasets/weather.json', 'a') as f:
    json.dump(weather_data, f, indent=4)
print("successfully saved 2016 May weather data in weather.json file")

api_url_06_2016 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2016-06-01:00&end_date=2016-07-01:00&tz=utc&key=d8398d8f101c45a5bd9847c85dfa8eb2"
response = requests.get(api_url_06_2016)
weather_data = response.json()
with open('Datasets/weather.json', 'a') as f:
    json.dump(weather_data, f, indent=4)
print("successfully saved 2016 June weather data in weather.json file")

api_url_07_2016 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2016-07-01:00&end_date=2016-08-01:00&tz=utc&key=d8398d8f101c45a5bd9847c85dfa8eb2"
response = requests.get(api_url_07_2016)
weather_data = response.json()
with open('Datasets/weather.json', 'a') as f:
    json.dump(weather_data, f, indent=4)
print("successfully saved 2016 July weather data in weather.json file")

api_url_08_2016 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2016-08-01:00&end_date=2016-09-01:00&tz=utc&key=d8398d8f101c45a5bd9847c85dfa8eb2"
response = requests.get(api_url_08_2016)
weather_data = response.json()
with open('Datasets/weather.json', 'a') as f:
    json.dump(weather_data, f, indent=4)
print("successfully saved 2016 August weather data in weather.json file")

api_url_09_2016 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2016-09-01:00&end_date=2016-10-01:00&tz=utc&key=d8398d8f101c45a5bd9847c85dfa8eb2"
response = requests.get(api_url_09_2016)
weather_data = response.json()
with open('Datasets/weather.json', 'a') as f:
    json.dump(weather_data, f, indent=4)
print("successfully saved 2016 September weather data in weather.json file")

api_url_10_2016 = "https://api.weatherbit.io/v2.0/history/subhourly?lat=36.17497&lon=-115.1372&start_date=2016-10-01:00&end_date=2016-11-01:00&tz=utc&key=d8398d8f101c45a5bd9847c85dfa8eb2"
response = requests.get(api_url_10_2016)
weather_data = response.json()
with open('Datasets/weather.json', 'a') as f:
    json.dump(weather_data, f, indent=4)
print("successfully saved 2016 October weather data in weather.json file")