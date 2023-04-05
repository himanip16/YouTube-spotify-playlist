import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import spotipy
import spotipy.util as util

# Set up YouTube API credentials
from spotipy import SpotifyOAuth

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "client_secret.json"


def empty_liked_playlist():
    scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

    # Use the client_secrets.json file to identify the application requesting
    # authorization. The client ID (from that file) and access scopes are required.
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        'client_secret.json',
        scopes=scopes)

    # Authenticate and authorize the user via local server
    credentials = flow.run_local_server(port=8080)
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    response = youtube.channels().list(
        part='contentDetails',
        mine=True
    ).execute()
    playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['likes']

    request = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlist_id,
        maxResults=50
    )

    nextPageToken = ''
    while True:
        request = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=nextPageToken
        )
        response = request.execute()
        items = response['items']
        if not items:
            break

        # Remove each video from the playlist
        for item in items:
            print(item['snippet']['resourceId'])
            video_id = item['snippet']['resourceId']['videoId']
            request = youtube.playlistItems().delete(
                id=item['id']
            )
            request.execute()

        # Get next page
        if 'nextPageToken' in response:
            nextPageToken = response['nextPageToken']
        else:
            break


def add_liked_songs_to_spotify():
    scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

    # Use the client_secrets.json file to identify the application requesting
    # authorization. The client ID (from that file) and access scopes are required.
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        'client_secret.json',
        scopes=scopes)

    # Authenticate and authorize the user via local server
    credentials = flow.run_local_server(port=8080)
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    # Set up Spotify API credentials
    SPOTIPY_CLIENT_ID = os.environ.get('SPOTIPY_CLIENT_ID')
    SPOTIPY_CLIENT_SECRET = os.environ.get('SPOTIPY_CLIENT_SECRET')
    SPOTIPY_REDIRECT_URI = os.environ.get('SPOTIPY_REDIRECT_URI')
    username = os.environ.get('SPOTIFY_USERNAME')
    scope = 'playlist-modify-public'
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=SPOTIPY_CLIENT_ID,
            client_secret=SPOTIPY_CLIENT_SECRET,
            redirect_uri=SPOTIPY_REDIRECT_URI,
            scope=scope,
        )
    )

    # Get list of videos in YouTube liked playlist
    playlist_name = "YouTube Liked Songs"
    user_id = sp.me()['id']
    playlist = sp.user_playlist_create(user=user_id, name=playlist_name)
    response = request.execute()

    # Iterate through each video and add corresponding track to Spotify playlist
    while response:
        for item in response['items']:
            video_title = item['snippet']['title']
            video_artist = item['snippet']['videoOwnerChannelTitle']
            query = f"{video_title} {video_artist}"
            search_results = sp.search(q=query, type='track')
            if search_results['tracks']['items']:
                track_uri = search_results['tracks']['items'][0]['uri']
                sp.playlist_add_items(playlist_id=playlist['id'],
                                      items=[track_uri])
        if 'nextPageToken' in response:
            request = youtube.playlistItems().list(
                part="snippet",
                playlistId=playlist_id,
                maxResults=50,
                pageToken=response['nextPageToken']
            )
            response = request.execute()
        else:
            break

    print("All videos in YouTube liked playlist have been added to Spotify playlist.")
