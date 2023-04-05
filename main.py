import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import spotipy
import spotipy.util as util
from spotipy import SpotifyOAuth
from spotifyPlaylist import get_existing_spotify_playlist, add_yt_playlist_songs_to_spotify
from youtubePlaylist import get_playlist_id

if __name__ == '__main__':
    # add_liked_songs_to_spotify()
    # get_youtube_playlists()
    # add_yt_playlists_songs_to_spotify()
    # get_existing_spotify_playlist()
    add_yt_playlist_songs_to_spotify()
