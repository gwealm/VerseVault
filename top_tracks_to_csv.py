import pandas as pd
import re


with open('top_tracks.txt','r+') as f:
    file = f.read()
    matches = re.findall("Artist: (.*), Track: (.*)", file)
    

# Create a Pandas DataFrame
df = pd.DataFrame(matches, columns=['Artist', 'Track'])

# Specify the file name for the CSV
csv_filename = 'music_data.csv'

# Write the DataFrame to a CSV file
df.to_csv(csv_filename, index=False)

print(f'CSV file "{csv_filename}" has been created with the data.')
    
# make a script that reads from top_tracks.txt and converts it to a csv
# df = pd.read_csv('top_tracks.txt', sep=',', names=['artist', 'track'])
# print(df.head())
# create a dataframe with pandas
# save the dataframe to a csv file
# df.to_csv('top_tracks.csv')