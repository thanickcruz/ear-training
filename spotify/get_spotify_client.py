import yaml
import spotipy
from spotipy import util
from spotipy.oauth2 import SpotifyOAuth

def spotify_oauth():
    '''
    Uses hidden client credentials object to get OAuth object
    '''
    with open('spotify/creds.yaml') as f:
    # Load the .yaml data
        info = yaml.load(f, Loader=yaml.FullLoader)

        # Spotify OAuth setup
        sp_oauth = SpotifyOAuth(
            client_id=info.get('client_id'),
            client_secret=info.get('client_secret'),
            redirect_uri="http://localhost:5000/callback",
            scope="user-library-read playlist-read-private playlist-read-collaborative",
            username='cruzn0215'
        )

        print('Connected to Spotify app!')
        
        return sp_oauth