from authentications import authenticate_spotify, authenticate_youtube
from youtubePlaylist import get_playlist_id


def create_spotify_playlist():
    # Get list of videos in Spotify playlist
    sp = authenticate_spotify()
    playlist_name = input("Name of Spotify playlist: ")
    user_id = sp.me()['id']
    playlist = sp.user_playlist_create(user=user_id, name=playlist_name)
    spotify_playlist_id = playlist['id']
    return spotify_playlist_id


def get_existing_spotify_playlist():
    sp = authenticate_spotify()
    playlists = sp.current_user_playlists()

    # Print playlist names and IDs
    for playlist in playlists['items']:
        print(f"{playlist['name']} - {playlist['id']}")

    spotify_playlist_id = input("Enter spotify Playlist Id from the list: ")
    return spotify_playlist_id


def add_yt_playlist_songs_to_spotify():
    sp = authenticate_spotify()
    youtube = authenticate_youtube()

    yt_playlist_id = get_playlist_id(youtube)

    request = youtube.playlistItems().list(
        part="snippet",
        playlistId=yt_playlist_id,
        maxResults=50
    )
    response = request.execute()

    playlist_choice = input("Type 1 for creating new Spotify playlist and 2 to use existing playlist: ")

    if playlist_choice == "1":
        spotify_playlist_id = create_spotify_playlist()
    else:
        spotify_playlist_id = get_existing_spotify_playlist()

    # Iterate through each video and add corresponding track to Spotify playlist
    while response:
        for item in response['items']:
            print(item['snippet'])
            video_title = item['snippet']['title']
            video_artist = item['snippet']['videoOwnerChannelTitle']
            query = f"{video_title} {video_artist}"
            search_results = sp.search(q=query, type='track')
            if search_results['tracks']['items']:
                track_uri = search_results['tracks']['items'][0]['uri']
                sp.playlist_add_items(playlist_id=spotify_playlist_id,
                                      items=[track_uri])
        if 'nextPageToken' in response:
            request = youtube.playlistItems().list(
                part="snippet",
                playlistId=yt_playlist_id,
                maxResults=50,
                pageToken=response['nextPageToken']
            )
            response = request.execute()
        else:
            break

    print("All videos in YouTube liked playlist have been added to Spotify playlist.")
