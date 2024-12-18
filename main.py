#!/usr/bin/python3

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import sys
import time

load_dotenv()
scope = "user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

def format(ms):
    seconds, _ = divmod(ms, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    result = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return result

albums = []
def get_album_info():
    print("fetching information from spotify...")
    global albums

    initial_time = time.perf_counter()
    results = sp.current_user_saved_albums(limit=50)
    albums = results['items']
    while results['next']:
        results = sp.next(results)
        albums.extend(results['items'])

    print(f"fetching finished in {(time.perf_counter() - initial_time):0.2f} seconds")

def print_info():
    for album in albums:
        album = album['album']

        duration = 0
        for track in album['tracks']['items']:
            duration += track['duration_ms']
        print(album['name'], "-", album['artists'][0]['name'], format(duration))

def output_csv(filename):
    formatted = '"Album","Artist","Duration","Total Length",\n'

    formula_added = False
    for album in albums:
        album = album['album']
        duration = 0
        for track in album['tracks']['items']:
            duration += track['duration_ms']
        
        formatted += f'"{album['name']}","{album['artists'][0]['name']}","{format(duration)}",'

        if not formula_added:
            formatted += f'"=SUM(C2:C{len(albums) + 1})"'
            formula_added = True

        formatted += '\n'

    with open(filename, 'w') as file:
        file.write(formatted)

get_album_info()

if len(sys.argv) == 2:
    output_csv(sys.argv[1])
else:
    print_info()