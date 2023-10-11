from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import requests
import csv

DATA_DIR = "./data/"

reader = csv.reader(open(DATA_DIR + "track_info.csv", 'r'))
writer = csv.writer(open(DATA_DIR + "track_lyrics.csv", 'w'), quoting=csv.QUOTE_NONNUMERIC)

writes = []

# Function to fetch lyrics for a single track
def fetch_lyrics(index, row):
    """
    Fetches lyrics for a given track and artist using a local API.

    Args:
        index (int): The index of the row in the DataFrame.
        row (pandas.Series): The row of the DataFrame containing the track and artist information.

    Returns:
        None
    """
    
    artist_name = row[3]
    track_name = row[0]

    api_url = f'http://localhost:3000/api/{track_name}/{artist_name}'
    while True:
        try:
            response = requests.get(api_url, timeout=10)
            break
        except InterruptedError as e:
            raise e
        except:
            print(f"Request for {track_name} by {artist_name} failed")
    
    if response.status_code == 200:
        lyrics_data = response.json()
        lyrics = lyrics_data.get('lyrics', 'Lyrics not found')
        print(f"Iteration {index}: successful")
        return [index, *row, lyrics]
    else:
        print(f"Iteration {index}: Failed")
        return [index, *row, "API request failed"]


if __name__ == '__main__':


    # Define the maximum number of threads (you can adjust this)
    MAX_THREADS = 32

    # Create a ThreadPoolExecutor with the specified number of threads
    with ThreadPoolExecutor(MAX_THREADS) as executor:
        # Iterate through each row in the DataFrame and submit tasks
        futures = [executor.submit(fetch_lyrics, index, row) for index, row in enumerate(reader)]

        # Wait for all tasks to complete
        for future in futures:
            writer.writerow(future.result())

    print(f'CSV file "{DATA_DIR + "track_lyrics.csv"}" has been created with lyrics.')
