# Set up YouTube API credentials
import os

import google_auth_oauthlib
import googleapiclient
import spotipy
from spotipy import SpotifyOAuth

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "client_secret.json"


def authenticate_youtube():
    scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        'client_secret.json',
        scopes=scopes)
    credentials = flow.run_local_server(port=8080)
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)
    return youtube


def authenticate_spotify():
    scopes = ["playlist-modify-public"]
    client_id = os.environ.get('SPOTIPY_CLIENT_ID')
    client_secret = os.environ.get('SPOTIPY_CLIENT_SECRET')
    redirect_uri = os.environ.get('SPOTIPY_REDIRECT_URI')
    username = os.environ.get('SPOTIFY_USERNAME')
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope=scopes,
        )
    )
    return sp

