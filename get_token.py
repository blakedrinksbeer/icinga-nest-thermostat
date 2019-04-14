#!/usr/bin/python3

import requests,argparse,sys

'''
Create a token which can be used in config.yaml
As of the time of writing this, they expire every 10 years.

This is terrifying, right?

If you need help getting started with the Nest API, see
this document from Google:
https://codelabs.developers.google.com/codelabs/wwn-api-quickstart/

Go to the "Authorization URL" from the OAuth client overview
in the Nest developer portal, follow the link and sign in
to your Nest account. The needed PIN will be presented there.
'''

parser = argparse.ArgumentParser(description="Setup OAuth token for Nest user.")
parser.add_argument("-i",metavar="client_id",required=True,help="Client ID for OAuth.")
parser.add_argument("-s",metavar="secret",required=True,help="Client Secret for OAuth.")
parser.add_argument("-p",metavar="pin",required=True,help="PIN Authorization for account.")
args = parser.parse_args()

if args.n:
    filename = f"{args.n}_token.json"
else:
    filename = "nest_token.json"

payload = {
    'client_id': args.i,
    'client_secret': args.s,
    'grant_type': 'authorization_code',
    'code': args.p
}

r = requests.post("https://api.home.nest.com/oauth2/access_token",data=payload)
if r.status_code != 200:
    print("Incorrect status code returned from server.")
    print(r.status_code)
    print(r.content)
    sys.exit(3)

j = r.json()
print(j['access_token'])    
