from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import requests

DATA_DIR = "../data/"

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
    artist_name = row['Artist']
    track_name = row['Track']

    api_url = f'http://localhost:3000/api/{track_name}/{artist_name}'
    response = requests.get(api_url, timeout=10)
    
    if response.status_code == 200:
        lyrics_data = response.json()
        lyrics = lyrics_data.get('lyrics', 'Lyrics not found')
        df.at[index, 'lyrics'] = lyrics
        print(f"Iteration {index}: successful")
    else:
        df.at[index, 'lyrics'] = 'API request failed'
        print(f"Iteration {index}: Failed")

# Load the CSV into a DataFrame
csv_filename = 'music_data.csv'

if __name__ == '__main__':

    df = pd.read_csv(csv_filename)

    # Create a new empty "lyrics" column in the DataFrame
    df['lyrics'] = ""

    # Define the maximum number of threads (you can adjust this)
    MAX_THREADS = 32

    # Create a ThreadPoolExecutor with the specified number of threads
    with ThreadPoolExecutor(MAX_THREADS) as executor:
        # Iterate through each row in the DataFrame and submit tasks
        futures = [executor.submit(fetch_lyrics, index, row) for index, row in df.iterrows()]

        # Wait for all tasks to complete
        for future in futures:
            future.result()

    # Save the updated DataFrame with the "lyrics" column to a new CSV file
    OUT_CSV = DATA_DIR + 'music_data_with_lyrics.csv'
    df.to_csv(OUT_CSV, index=False)

    print(f'CSV file "{OUT_CSV}" has been created with lyrics.')
