import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()
scope = "user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

def format(ms):
    seconds, _ = divmod(ms, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    result = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return result

def print_info():
    results = sp.current_user_saved_albums(limit=50)
    
    albums = results['items']
    while results['next']:
        results = sp.next(results)
        albums.extend(results['items'])

    for album in albums:
        album = album['album']

        duration = 0
        for track in album['tracks']['items']:
            duration += track['duration_ms']
        print(album['name'], "-", album['artists'][0]['name'], " ", format(duration))

print_info()