from flask import Flask, render_template, send_from_directory, redirect, url_for, request, session
import random
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotify.get_spotify_client import spotify_oauth
import json
import random

import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)
app.secret_key = "yooo"  # Required for session management

# Get hidden spotify client credentials
sp_oauth=spotify_oauth()

# Path to the audio samples
SAMPLES_DIR = os.path.join(app.static_folder, 'samples')

# List of available audio files in the samples directory
sample_files = [f for f in os.listdir(SAMPLES_DIR) if f.endswith('.wav')]

# HELPER FUNCTION
def get_track_key(track_id):
    """
    Takes in track_id and returns key in same format as sample WAV files.
    """
    url=f'https://songdata.io/track/{track_id}'
    
    # Regular expression pattern to match key signatures like "Ab Minor", "D Major", etc.
    key_signature_pattern = r'\b([A-Ga-g])(#|b)?\s?(Major|Minor)\b'

    try:
    # Sending GET request
        response = requests.get(url)
    
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the response HTML
            soup = BeautifulSoup(response.text, 'html.parser')
        
            # Find all elements with the class 'card grid my-1 py-1'
            card_elements = soup.find_all(class_='card grid my-1 py-1')
        
            # Iterate through each element and search for key signatures
        for card in card_elements:
            # Search for key signature in the text of each card element
            match = re.search(key_signature_pattern, card.get_text())
            if match:
                note = match.group(1)
                accidental = match.group(2) or ''
                scale_type = match.group(3)
                
                # Format the key signature
                key_signature = f"{note}{accidental.lower()}{'m' if scale_type == 'Minor' else ''}"
                    
                return key_signature
            else:
                print("No key signature found.")
        
        else:
            print(f"Failed to retrieve data. HTTP Status Code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")
# get_track_key

# HELPER FUNCTION
def get_random_track(sp):
    """
    Selects a random track from a random user's playlist and returns its ID and key signature.

    Parameters:
        sp (spotipy.Spotify): An authenticated Spotipy client object.

    Returns:
        dict: A dictionary with 'track_id', 'key_signature'.
    """
    # Get the current user's playlists
    playlists = sp.current_user_playlists()
    if not playlists['items']:
        return {"error": "No playlists found for the user."}

    # Select a random playlist
    random_playlist = random.choice(playlists['items'])
    playlist_id = random_playlist['id']

    # Get tracks in the selected playlist
    playlist_tracks = sp.playlist_tracks(playlist_id)
    if not playlist_tracks['items']:
        return {"error": "No tracks found in the playlist."}

    # Select a random track from the playlist
    random_track = random.choice(playlist_tracks['items'])['track']
    track_id = random_track['id']
    
    key_signature = get_track_key(track_id)

    return {'track_id':track_id,'key_signature':key_signature}


# Initialize session variables if not set
def initialize_session():
    if 'correct_answers' not in session:
        session['correct_answers'] = 0
    if 'total_samples' not in session:
        session['total_samples'] = 0
    if 'response_log' not in session:
        session['response_log'] = {}  # Track responses per sample

@app.route('/')
def index():
    initialize_session()  # Ensure session variables are set
    sample = random.choice(sample_files)
    return render_template('index.html', sample=sample, result=None, result_color=None, score=None)


@app.route('/tracks')
def tracks():
    initialize_session()  # If session variables are needed

    # Get the token from session
    token_info = session.get('token_info', None)
    if not token_info:
        return redirect(url_for('login'))  # Redirect to Spotify login if token is missing

    sp = spotipy.Spotify(auth=token_info['access_token'])
    
    # Check if token is expired and refresh it
    if sp_oauth.is_token_expired(token_info):
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
        session['token_info'] = token_info
        sp = spotipy.Spotify(auth=token_info['access_token'])  # Re-initialize with the refreshed token

    try:
        track_info=get_random_track(sp)
        track_id=track_info['track_id']
        key_signature=track_info['key_signature']

    except spotipy.exceptions.SpotifyException as e:
        # Handle exceptions if any API error occurs
        print(f"Error fetching playlists: {e}")
        return "Failed to fetch playlists. Please try again later."

    return render_template('tracks.html',track_id=track_id, key_signature=key_signature,result=None, result_color=None, score=None)

@app.route('/login')
def login():
    # Redirect the user to Spotify's authorization URL
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)

    # Debugging line to check token_info
    print(f"Token Info: {token_info}")

    session['token_info'] = token_info

    if sp_oauth.is_token_expired(token_info):
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
        session['token_info'] = token_info

    return redirect(url_for('tracks'))


@app.route('/static/samples/<filename>')
def serve_sample(filename):
    return send_from_directory(SAMPLES_DIR, filename)

@app.route('/guess', methods=['POST'])
def guess():
    initialize_session()

    enharmonic_map = {
        "A#": "Bb", "Bb": "A#",
        "C#": "Db", "Db": "C#",
        "D#": "Eb", "Eb": "D#",
        "F#": "Gb", "Gb": "F#",
        "G#": "Ab", "Ab": "G#",
        "A#m": "Bbm", "Bbm": "A#m",
        "C#m": "Dbm", "Dbm": "C#m",
        "D#m": "Ebm", "Ebm": "D#m",
        "F#m": "Gbm", "Gbm": "F#m",
        "G#m": "Abm", "Abm": "G#m"
    }

    user_guess = request.form.get('user_guess').strip()
    sample = request.form.get('sample')

    chord = sample.split('_')[0]

    if 'response_log' not in session:
        session['response_log'] = {}

    session['total_samples'] += 1

    if user_guess == chord or enharmonic_map.get(user_guess) == chord:
        session['correct_answers'] += 1
        result = "Correct"
    else:
        result = "Incorrect"

    # Ensure each sample logs result and guessed response
    session['response_log'][sample] = (result, user_guess)

    score = f"{session['correct_answers']} / {session['total_samples']}"

    return render_template('index.html', sample=sample, result=result, result_color="green" if result == "Correct" else "red", score=score)


@app.route('/guess_track', methods=['POST'])
def guess_track():
    initialize_session()

    enharmonic_map = {
        "A#": "Bb", "Bb": "A#",
        "C#": "Db", "Db": "C#",
        "D#": "Eb", "Eb": "D#",
        "F#": "Gb", "Gb": "F#",
        "G#": "Ab", "Ab": "G#",
        "A#m": "Bbm", "Bbm": "A#m",
        "C#m": "Dbm", "Dbm": "C#m",
        "D#m": "Ebm", "Ebm": "D#m",
        "F#m": "Gbm", "Gbm": "F#m",
        "G#m": "Abm", "Abm": "G#m"
    }
    track_id=request.form.get('track_id')
    user_guess = request.form.get('user_guess').strip()
    chord = request.form.get('key_signature')

    if 'response_log' not in session:
        session['response_log'] = {}

    session['total_samples'] += 1

    if user_guess == chord or enharmonic_map.get(user_guess) == chord:
        session['correct_answers'] += 1
        result = "Correct"
    else:
        result = "Incorrect"
    
    # Ensure each sample logs result and guessed response
    session['response_log'][chord] = (result, user_guess)

    score = f"{session['correct_answers']} / {session['total_samples']}"

    return render_template('tracks.html', track_id=track_id, key_signature=chord, result=result, result_color="green" if result == "Correct" else "red", score=score)


@app.route('/next')
def next_sample():
    initialize_session()  # Ensure session variables are set
    sample = random.choice(sample_files)
    return render_template('index.html', sample=sample, result=None, result_color=None, score=f"{session['correct_answers']} / {session['total_samples']}")

@app.route('/next_track')
def next_track_sample():
    initialize_session()  # Ensure session variables are set

    # Get the token from session
    token_info = session.get('token_info', None)
    if not token_info:
        return redirect(url_for('login'))  # Redirect to login if no token exists

    # Rebuild the Spotify client using the access token
    sp = spotipy.Spotify(auth=token_info['access_token'])

    # Check if token is expired and refresh it
    if sp_oauth.is_token_expired(token_info):
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
        session['token_info'] = token_info
        sp = spotipy.Spotify(auth=token_info['access_token'])  # Re-initialize with the refreshed token

    try:
        track_info = get_random_track(sp)
        track_id = track_info['track_id']
        key_signature = track_info['key_signature']

    except spotipy.exceptions.SpotifyException as e:
        # Handle exceptions if any API error occurs
        print(f"Error fetching playlists: {e}")
        return "Failed to fetch playlists. Please try again later."

    return render_template('tracks.html', track_id=track_id, key_signature=key_signature, result=None, result_color=None, score=f"{session['correct_answers']} / {session['total_samples']}")

@app.route('/log')
def log():
    initialize_session()  # Ensure session variables are set
    return render_template('log.html', response_log=session['response_log'])

@app.route('/track_log')
def track_log():
    initialize_session()  # Ensure session variables are set
    return render_template('track_log.html', response_log=session['response_log'])

if __name__ == '__main__':
    app.run(debug=True)
