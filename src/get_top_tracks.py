import requests
from dotenv import load_dotenv
import os
import time
import pprint
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

    # Create a Pandas DataFrame
    top_tracks_df = pd.DataFrame(columns=['Artist', 'Track'])

    max_page_number = 1000

    for i in range(1,max_page_number):
        # Send a GET request to the Last.fm API
        response = requests.get(endpoint + f"&page={i}")

        if response.status_code == 200:
            data = response.json()
            pprint.pprint(data)
            top_tracks = data['tracks']['track']

            # Iterate through the top tracks and print artist and track names
            for track in top_tracks:
                artist_name = track['artist']['name']
                track_name = track['name']
                top_tracks_df = top_tracks_df.add({'Artist': artist_name, 'Track': track_name})
                print(f'Artist: {artist_name}, Track: {track_name}\n')

        time.sleep(1)
        
    else:
        print('Failed to retrieve top tracks.')
        
    # Save the DataFrame to a CSV file
    top_tracks_df.to_csv('top_tracks.csv', index=False)

