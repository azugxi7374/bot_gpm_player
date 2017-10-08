# ref: http://unofficial-google-music-api.readthedocs.io/en/latest/reference/mobileclient.html

from getpass import getpass
import os
from gmusicapi import Mobileclient

USER_ENV = "PI1_GOOGLE_USER"
PASS_ENV = "PI1_GOOGLE_PASS"

user_name = os.getenv(USER_ENV)
user_pass = os.getenv(PASS_ENV)
if user_name is None: user_name = input("PI1_GOOGLE_USER: ")
if user_pass is None: user_pass = getpass("PI1_GOOGLE_PASS: ")

api = Mobileclient()
login_ok = api.login(user_name, user_pass, Mobileclient.FROM_MAC_ADDRESS)
print("login: ", login_ok)

plist = api.get_station_tracks('IFL')

print(plist[0])
print(api.get_stream_url(plist[0]['storeId']))

"""
for t in plist:
    url = api.get_stream_url(t['storeId'])
    print(url)
"""
print("ok!")
