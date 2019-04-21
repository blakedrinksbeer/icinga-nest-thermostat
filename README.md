# icinga-nest-thermostat


An Icinga/Nagios compatible plugin for monitoring ambient/outdoor temperatures and comparing them against current thermostat settings. Ideally this is to be used with a time series database such as Graphite/Carbon for graphing.

---
### Requirements:
* Python 3.6+
* python-requests
* PyYAML
* A Nest developer account

This has been tested using Icinga2, Graphite and Grafana. 

### Getting a Nest OAuth token:
Google has a very simple walkthrough on getting your Nest developer account setup:
[Works with Nest API Quick Start Guide](https://codelabs.developers.google.com/codelabs/wwn-api-quickstart/)

There is a script I've provided to help you get your OAuth key in order. Once you have the client ID and client secret, login to the link they provide you and get your pin. Enter that into ```get_token.py``` and it will get your OAuth key for you.
```
usage: get_token.py [-h] -i client_id -s secret -p pin

Setup OAuth token for Nest user.

optional arguments:
  -h, --help    show this help message and exit
  -i client_id  Client ID for OAuth.
  -s secret     Client Secret for OAuth.
  -p pin        PIN Authorization for account.
```

Take the OAuth token you receive and paste it into your config.yaml.
```
# Token for nest to work
nest_token: c.bunchofgibberishhere
```

### Command usage:
```
usage: check_nest_thermostat.py [-h] [-c yaml file] [-u C/F] [-s name]
                                [-n name] [-w module]

Monitor statistics of Nest Thermostat.

optional arguments:
  -h, --help    show this help message and exit
  -c yaml file  Path to file with OAuth token (defaults to ./config.yaml)
  -u C/F        Celcius or Faherenheit, defaults to Nest setting.
  -s name       What you named this domicile (e.g. Your Mom's House Bitch),
                defaults to the first one it finds.
  -n name       What you named this thermostat (e.g. Living Room), defaults to
                the first one it finds.
  -w module     Use a plugin for outdoor weather details.
```
If you're not collecting data about outdoor weather, this should probably just work.

### Outdoor conditions:
Although Nest uses AccuWeather to show the outdoor weather on your thermostat, this info is not in the json output from their API, so you'll need an alternative source for outdoor weather information. I've setup two modules for this so far, each returns perfdata for temperature and humidity values. It's straight forward and you can easily create your own for different weather APIs. I'm considering buying a weather station for better accuracy.

##### openweathermap.org:
```
-w openweathermap
```

OpenWeatherMap offers free API keys for simple projects like this. You can get an account here: [https://home.openweathermap.org/users/sign_up](https://home.openweathermap.org/users/sign_up)

When that's setup, add the api key to config.yaml:
```
owm_api_key: yourapikey
owm_city_id: 4930956
```

The example city_id there is for Boston. Search for your city on the website and you'll see the ID in the URL.

This updates very frequently and will give you up to date data, but it seems like whatever station they're using in Boston must be sitting in direct sunlight. It's accurate as long as it's overcast or dark, then 10 degrees over the rest of the time. I'm using the free National Weather Service API instead.

##### weather.gov:
```
-w weathergov
```
This one is only useful in the United States. It doesn't require an API key or an account. It doesn't update as often as OpenWeatherMap, but it's accurate and gets the job done.

[API Web Service](https://www.weather.gov/documentation/services-web-api)
Skim the documentation here. You'll want to put in your coordinates under /points/ to find the nearest list of weather stations, then add this to config.yaml. Below is an example using Boston Logan Airport's weather station:

```
# weather_gov weather.gov
wgov_station: KBOS
```

### Example files:

A few templates have been provided.
##### config.yaml-example
Pretty much things summarized above. Put in any needed API keys or weather station info here.
##### icinga-example.conf
Host/Service/Command object templates for Icinga2.
##### nest-icinga-graphite.ini
If you have the icingaweb2 Graphite module installed, copy this to ```/etc/icingaweb2/enabledModules/graphite/templates/``` for pretty output.