# example url
# http://api.openweathermap.org/data/2.5/forecast?q=minneapolis,us&units=imperial&appid=a4384a8fae04ffee4382984f5e28507a

import os
import requests
from datetime import datetime
import logging

logging.basicConfig(filename='debug.log', level=logging.DEBUG, format=f'%(asctime)s - %(levelname)s - %(message)s')
key = os.environ.get('WEATHER_KEY')
url = 'http://api.openweathermap.org/data/2.5/forecast'

def main():
    try:
        location = get_location()
        forecast = get_forecast_data(location, key)
        display_forecast(forecast, location)
    except TypeError as te:
        print(f'There was a problem getting the location.')
        logging.debug(f'An error getting the location: {te}')
        


def get_location():
    city, country = '', ''
    while len(city) == 0:
        city = input('Enter the name of the city: ').strip().upper()
    while len(country) != 2 or not country.isalpha():
        country = input('Enter the 2-letter country code: ').strip().upper()

    location = f'{city},{country}'
    return location


def get_forecast_data(location, key):
    try:
        query = {'q': location, 'units': 'imperial', 'appid': key}
        response = requests.get(url, params=query)
        response.raise_for_status() # raise exception for 400 or 500 errors
        data = response.json() # this may error too, if response is not JSON
        return data
    
    except Exception as e:
        print(f'There was a problem getting the forecast data.')
        logging.debug(f'Error getting forecast data: {e}')


def display_forecast(forecast_data, location):
    try:
        list_of_forecasts = forecast_data['list']
        print(f'\nWeather for {location}')
        for forecast in list_of_forecasts:
            temp = forecast['main']['temp']
            wind_speed = forecast['wind']['speed']
            weather = forecast['weather'][0]
            description = weather['description']
            """
            UTC time because it can convert timestramps
            to the local time. So if I was in a different time zone,
            this program should still show the time that I am in. 
            """
            timestamp = forecast['dt']
            date_and_time = datetime.fromtimestamp(timestamp)
            print('------------------------------------------------------------------')
            print(f'{date_and_time} | Temp: {temp:.0f}F | Wind speed: {wind_speed:.0f} | {description}')

    except KeyError as ke:
        print('This data is not in the format expected')
        logging.debug(f'Error in displaying forecast: {ke}')

if __name__ == '__main__':
    main()