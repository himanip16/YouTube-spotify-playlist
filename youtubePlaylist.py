import os

import google_auth_oauthlib
import googleapiclient

from authentications import authenticate_youtube


def get_youtube_playlists():
    youtube = authenticate_youtube()
    return get_youtube_playlists(youtube)


def get_youtube_playlists(youtube):
    # Call the playlists().list() method to get a list of all playlists
    playlists = []
    next_page_token = None
    while True:
        request = youtube.playlists().list(
            part="snippet",
            mine=True,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()
        playlists.extend(response["items"])
        print(response["items"])
        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    # Print the title and ID of each playlist
    playlist_map = {}
    index = 1
    for playlist in playlists:
        playlist_map[playlist['snippet']['title']] = playlist['id']
        print(f"{index}. {playlist['snippet']['title']}: {playlist['id']}")
        index += 1

    return playlist_map


def get_playlist_id(youtube):
    playlist_map = get_youtube_playlists(youtube)
    playlist_name = input("Select name of the playlist")
    return playlist_map[playlist_name]


def youtube_liked_playlist_id():
    youtube = authenticate_youtube()

    response = youtube.channels().list(
        part='contentDetails',
        mine=True
    ).execute()
    youtube_playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['likes']
    return youtube_playlist_id


def delete_all_songs_liked_playlist(youtube_playlist_id):
    youtube = authenticate_youtube()

    next_page_token = ''
    while True:
        request = youtube.playlistItems().list(
            part="snippet",
            playlistId=youtube_playlist_id,
            maxResults=50,
            pageToken=next_page_token
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
            next_page_token = response['nextPageToken']
        else:
            break
