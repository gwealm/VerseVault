import json
import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor

# Function to fetch lyrics for a single track
def fetch_lyrics(index, row):
    artist_name = row['Artist']
    track_name = row['Track']
    
    api_url = f'http://localhost:3000/api/{track_name}/{artist_name}'
    response = requests.get(api_url)
    
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
df = pd.read_csv(csv_filename)

# Create a new empty "lyrics" column in the DataFrame
df['lyrics'] = ""

# Define the maximum number of threads (you can adjust this)
max_threads = 32

# Create a ThreadPoolExecutor with the specified number of threads
with ThreadPoolExecutor(max_threads) as executor:
    # Iterate through each row in the DataFrame and submit tasks
    futures = [executor.submit(fetch_lyrics, index, row) for index, row in df.iterrows()]

    # Wait for all tasks to complete
    for future in futures:
        future.result()

# Save the updated DataFrame with the "lyrics" column to a new CSV file
output_csv_filename = 'music_data_with_lyrics.csv'
df.to_csv(output_csv_filename, index=False)

print(f'CSV file "{output_csv_filename}" has been created with lyrics.')
