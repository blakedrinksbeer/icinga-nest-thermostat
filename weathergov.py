#!/usr/bin/python3
import requests

def weather(config,unit):

    station = config['wgov_station']

    r = requests.get(f'https://api.weather.gov/stations/{station}/observations/latest')

    w = r.json()

    humidity = w['properties']['relativeHumidity']['value']
    temperature = w['properties']['temperature']['value']

    if humidity:
        output = f'outside_humidity={humidity:.2f}%;;;0;100 '

    if temperature:
        if unit == 'F':
            temperature = (temperature * 1.8) + 32
        output += f'outside_temp={temperature:.2f} '
    
    return(output)
