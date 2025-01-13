# Ear Training Game

Welcome to my ear training project! This app tests your perfect pitch with chord samples and songs.

# SETUP

## Create Spotify App and Configure Credentials
Create new app https://developer.spotify.com/dashboard and create `spotify/creds.yaml` file. In that file, paste your `client_id` and `client_secret`. **Ensure that these credentials are not publicly exposed.**


## Install packages.
`pip install -r requirements.txt`




#### Ideas
- Recommend songs in that key.
- Track progress and weaknesses

## Issues
- Thinks flat and sharp notation for same note is different (ie it thinks Ab is not also G#)
