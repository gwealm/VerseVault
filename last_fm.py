import requests
from dotenv import load_dotenv
import os
import time
import pprint

load_dotenv()

# get the API key from the .env file
LASTFM_API_KEY = os.getenv('LASTFM_API_KEY')

# numbers of tracks to be shown
TRACK_NO = 1000

# Define the Last.fm API endpoint for chart tracks
endpoint = f'http://ws.audioscrobbler.com/2.0/?method=chart.gettoptracks&limit={TRACK_NO}&api_key={LASTFM_API_KEY}&format=json'

print(endpoint)

for i in range(1,1000):
    # Send a GET request to the Last.fm API
    response = requests.get(endpoint + f"&page={i}")

    if response.status_code == 200:
        data = response.json()
        pprint.pprint(data)
        top_tracks = data['tracks']['track']

        # Iterate through the top tracks and print artist and track names
        with open('top_tracks.txt', 'a') as f:
            for track in top_tracks:
                artist_name = track['artist']['name']
                track_name = track['name']

                f.write(f'Artist: {artist_name}, Track: {track_name}\n')
                print(f'Artist: {artist_name}, Track: {track_name}\n')
    time.sleep(1)
    
else:
    print('Failed to retrieve top tracks.')

