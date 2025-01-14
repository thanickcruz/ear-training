import yaml
import spotipy
from spotipy import util
from spotipy.oauth2 import SpotifyOAuth
import os

def spotify_oauth():
    '''
    Uses hidden client credentials object to get OAuth object
    '''

    """ ALTERNATIVE YAML CASE
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
    """

    # Fetch credentials from environment variables
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI')

    if not client_id or not client_secret or not redirect_uri:
        raise ValueError("Spotify credentials are not set in environment variables.")

    # Spotify OAuth setup
    sp_oauth = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope="user-library-read playlist-read-private playlist-read-collaborative",
        username='cruzn0215'
    )

    print('Connected to Spotify app!')
    return sp_oauth
