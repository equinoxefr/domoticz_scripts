#! /usr/bin/python3

import requests
import argparse

parser = argparse.ArgumentParser(description='Tado presence setting')
parser.add_argument('--mode', help='Setting status HOME or AWAY',required=True)
parser.add_argument('--user', help='username',required=True)
parser.add_argument('--password', help='password',required=True)

args = vars(parser.parse_args())

resp = requests.post('https://auth.tado.com/oauth/token',params={ "client_id": "tado-web-app","grant_type": "password", "scope": "home.user", "username": args["user"], "password": args["password"], "client_secret": "wZaRN7rpjn3FoNyF5IFuxg9uMzYJcvOoQ8QWiIqS3hfk6gLhVlG57j5YNoZL2Rtc"})
if resp.status_code != 200:
    # This means something went wrong.
    print("ERROR {}".format(resp))
    exit(-1)
token = resp.json()["access_token"]
resp = requests.get('https://my.tado.com/api/v1/me',headers= { "Authorization": "Bearer " + token})
if resp.status_code != 200:
    # This means something went wrong.
    print("ERROR {}".format(resp))
    exit(-1)
homeId = resp.json()["homeId"]
resp = requests.get('https://my.tado.com/api/v2/homes/'+ str(homeId) +'/state',headers= { "Authorization": "Bearer " + token})
if resp.status_code != 200:
    # This means something went wrong.
    print("ERROR {}".format(resp))
    exit(-1)
print("Current status: {}".format(resp.json()["presence"]))
print("Setting to: {}".format(args["mode"]))
resp = requests.put('https://my.tado.com/api/v2/homes/'+ str(homeId) +'/presenceLock',headers= { "Content-Type": "application/json" , "Authorization": "Bearer " + token}, params= { "homePresence": args["mode"] })
if resp.status_code != 200 and resp.status_code != 204:
    # This means something went wrong.
    print("ERROR {}".format(resp))
    exit(-1)
print("Done")

