import time
import pprint
import os
import requests
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

# Get the API key from the .env file
LASTFM_API_KEY = os.getenv('LASTFM_API_KEY')

# Directory to save the data
DATA_DIR = "../data/"

# Specify the file name for the CSV
CSV_FILENAME = 'music_data.csv'

# Numbers of tracks to be shown
TRACK_NO = 1000

# Define the Last.fm API endpoint for chart tracks
endpoint = f'http://ws.audioscrobbler.com/2.0/?method=chart.gettoptracks&limit={TRACK_NO}&api_key={LASTFM_API_KEY}&format=json'


if __name__ == '__main__':

    # Create an empty list to store the data
    top_tracks_data = []

    MAX_PAGE_NUMBER = 1000

    for i in range(1,MAX_PAGE_NUMBER):
        # Send a GET request to the Last.fm API
        response = requests.get(endpoint + f"&page={i}", timeout=10)

        if response.status_code == 200:
            data = response.json()
            pprint.pprint(data)
            top_tracks = data['tracks']['track']

            # Iterate through the top tracks and print artist and track names
            for track in top_tracks:
                artist_name = track['artist']['name']
                track_name = track['name']

                top_tracks_data.append({'Artist': artist_name, 'Track': track_name})
                print(f'Artist: {artist_name}, Track: {track_name}')
        else:
            print('Failed to retrieve top tracks.')

        time.sleep(1)
        
        
    # Create a DataFrame from the list of data
    top_tracks_df = pd.DataFrame(top_tracks_data)

    # Save the DataFrame to a CSV file
    top_tracks_df.to_csv('top_tracks.csv', index=False)
