# ref: http://unofficial-google-music-api.readthedocs.io/en/latest/reference/mobileclient.html

from getpass import getpass
import os
from gmusicapi import Mobileclient
import urllib.request
import commands as cmd


USER_ENV = "GPM_GOOGLE_USER"
PASS_ENV = "GPM_GOOGLE_PASS"

def fileDownload(url, fileName):
    print("downloading ", url)
    urllib.request.urlretrieve(url, fileName)

def login(api):
    while(not api.is_authenticated()):
        user_name = os.getenv(USER_ENV)
        user_pass = os.getenv(PASS_ENV)
        if user_name is None: user_name = input(USER_ENV+": ")
        if user_pass is None: user_pass = getpass(PASS_ENV+": ")
    
        api.login(user_name, user_pass, Mobileclient.FROM_MAC_ADDRESS)
    return api

def findSongs(api, query):
    tracks = [x["track"] for x in api.search(query)["song_hits"]]

def getPlaylist(api, query):
    reslist = [plist["tracks"] for plist in api.get_all_user_playlist_contents() if query in plist["name"] if "tracks" in plist.keys()]
    
    if len(reslist) > 0:
        return [x["track"] for x in reslist[0] if "track" in x.keys()]
    else:
        return []

def getIFL(api):
    tracks = api.get_station_tracks('IFL')
    return tracks

def run(api, query):
    login(api)

    tracks = []
    if query == "":
        # IFL
        tracks = getIFL(api)
    else:
        tracks = getPlaylist(api, query)

    for t in tracks:
        print(disp(t))
        url = api.get_stream_url(t['storeId'])
        cmd.callPlay(url)
        # fileDownload(url, t["title"]+".mp3")
    print("ok")


def disp(track):
    return track.get("artist", "_") + ": \"" + track.get("title", "_") + "\", " + track.get("album", "_") + " (" + str(track.get("year", "_")) + ")"



if __name__ == "__main__":
    api = Mobileclient()
    while(True):
        query = input("query: ")
        run(api, query)


