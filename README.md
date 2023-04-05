# YouTube to Spotify Playlist Sync

This project is a Python script that uses the YouTube Data API and Spotify Web API to sync videos that you have liked on YouTube to a Spotify playlist.

## Prerequisites

Before you can run the script, you will need to have the following installed:

- Python 3.6 or later
- google-auth-oauthlib, google-auth, google-api-python-client, and spotipy Python packages
- A Spotify developer account and Spotify API credentials. You can obtain these here.
```
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client spotipy
```


You also need to set up the following credentials:

- YouTube API credentials
- Spotify API credentials

## Setup

### YouTube API Credentials

1. Go to the Google Developers Console.
2. Select your project or create a new one.
3. In the sidebar, select "Credentials".
4. Click "Create Credentials" and select "OAuth client ID".
5. Select "Desktop app" and give it a name.
6. Click "Create".
7. Click "Download" to download the client secrets file.
8. Save the client secrets file in the project directory.

### Spotify API Credentials

1. Go to the Spotify Developer Dashboard.
2. Log in to your account or create a new one.
3. Create a new app and give it a name.
4. Add http://localhost:8080 as a redirect URI in the app settings.
5. Copy the "Client ID" and "Client Secret" and save them as environment variables in your operating system with the names SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET.
6. In the app settings, add http://localhost:8080 as a redirect URI.


## Contributing

If you find a bug or have a suggestion, please open an issue or create a pull request.

