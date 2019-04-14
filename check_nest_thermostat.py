#!/usr/bin/python3

# If you do not have an OAuth key yet, check get_token.py and follow the
# instructions to create a developer account if you have not.
# https://codelabs.developers.google.com/codelabs/wwn-api-quickstart/

import requests,yaml,argparse,sys

parser = argparse.ArgumentParser(description="Monitor statistics of Nest Thermostat.")
parser.add_argument("-c",metavar="yaml file",help="Path to file with OAuth token (defaults to ./config.yaml)")
parser.add_argument("-u",metavar="C/F",help="Celcius or Faherenheit, defaults to Nest setting.")
parser.add_argument("-s",metavar="name",help="What you named this domicile (e.g. Your Mom's House Bitch), defaults to the first one it finds.")
parser.add_argument("-n",metavar="name",help="What you named this thermostat (e.g. Living Room), defaults to the first one it finds.")
parser.add_argument("-w",metavar="module",help="Use a plugin for outdoor weather details.")
args = parser.parse_args()

# Load the relevant weather module.
if args.w == 'openweathermap':
    from openweathermap import weather

if args.c:
    configfile = args.c
else:
    configfile = "config.yaml"

try:
    with open(configfile,'r') as f:
        config = yaml.load(f.read())

    token = config['nest_token']
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    
except Exception as e:
    print("Unable to load OAuth token.")
    print(e)
    sys.exit(3)
    
s = requests.session()
s.headers.update(headers)

# Because for whatever reason python-requests doesn't _really_ follow the redirect
# like its supposed to, and the redirect url needs to be fetched with headers
# submitted instead. I might just be a fucking idiot, though. Very possible.
geturl = s.get('https://developer-api.nest.com/',allow_redirects=False)
redurl = geturl.headers['location']

nestdump = s.get(redurl).json()
thermostats = nestdump['devices']['thermostats']
structures = nestdump['structures']

# Predefine nest variables
ti = False
structure = False

# Structure dict holds away/home information
for s in structures:
    if not args.s:
        structure = structures[s]
        break
    elif structures[s]['name'] == args.s:
        structure = structures[s]
        break

if not structure:
    print("Structure not found")
    sys.exit(3)

# Get the individual thermostat associated with the prior structure
for t in structure['thermostats']:
    if not args.n:
        ti = thermostats[t]
        break
    elif thermostats[t]['where_name'] == args.n:
        ti = thermostats[t]
    
if not ti:
    print("Thermostat not found")
    sys.exit(3)

if args.u and (args.u.lower() == "c" or args.u.lower() == "f"):
    u = args.u.lower()
else:
    u = ti['temperature_scale'].lower()

ambient = ti[f'ambient_temperature_{u}']
humidity = ti['humidity']
hvacmode = ti['hvac_mode']

perfdata = f"humidity={humidity}%;;;0;100 ambient={ambient} "

if ti['hvac_state'] == 'off':
    perfdata += "hvacstate=0 "
else:
    perfdata += "hvacstate=1 "

if structure['away'] == 'home':
    perfdata += "home=1 "
else:
    perfdata += "home=0 "
    
if hvacmode == 'eco':
    ecolow = ti[f'eco_temperature_low_{u}']
    ecohigh = ti[f'eco_temperature_high_{u}']
    perfdata += f"ecolow={ecolow} ecohigh={ecohigh} "
elif hvacmode == 'heat' or hvacmode == 'cool':
    targettemp = ti[f'target_temperature_{u}']
    perfdata += f"{hvacmode}={targettemp} "
elif hvacmode == 'heat-cool':
    heat = ti[f'target_temperature_high_{u}']
    cool = ti[f'target_temperature_low_{u}']
    perfdata += f"heat={heat} cool={cool} "

if args.w:
    currentweather = weather(config,ti['temperature_scale'])
    perfdata += currentweather
    
print(perfdata)
