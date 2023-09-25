import json
import pandas as pd
import requests

# Load the CSV into a DataFrame
csv_filename = 'music_data.csv'
df = pd.read_csv(csv_filename)

# Create a new empty "lyrics" column in the DataFrame
df['lyrics'] = ""

i = 0
# Iterate through each row in the DataFrame
for index, row in df.iterrows():

    artist_name = row['Artist']
    track_name = row['Track']
    
    # Make a request to the Lyrist API
    api_url = f'http://localhost:3000/api/{track_name}/{artist_name}'
    response = requests.get(api_url)
    
    if response.status_code == 200:
        lyrics_data = response.json()
        lyrics = lyrics_data.get('lyrics', 'Lyrics not found')
        df.at[index, 'lyrics'] = lyrics
        print(f"Iteration {i}: successfull")
    else:
        df.at[index, 'lyrics'] = 'API request failed'
        print(f"Iteration {i}: Kill me please")
    
    i += 1

# Save the updated DataFrame with the "lyrics" column to a new CSV file
output_csv_filename = 'music_data_with_lyrics.csv'
df.to_csv(output_csv_filename, index=False)

print(f'CSV file "{output_csv_filename}" has been created with lyrics.')