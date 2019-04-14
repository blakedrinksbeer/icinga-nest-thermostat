#!/usr/bin/python3
import requests

def weather(config,unit):

    if unit == 'F':
        unit = 'imperial'
    else:
        unit = 'metric'

    api = config['owm_api_key']
    city = config['owm_city_id']

    r = requests.get(f'http://api.openweathermap.org/data/2.5/weather?id={city}&APPID={api}&units={unit}')

    w = r.json()

    humidity = w['main']['humidity']
    temperature = w['main']['temp']
    
    return(f'outside_humidity={humidity};;0;100 outside_temp={temperature} ')
