import csv
import re
import json
import sys

def main():
    
        sections_regex = re.compile(r"\[(.*?)]\n(.*?)(?=$|\n\[)", re.U | re.S)
    
        reader = csv.DictReader(sys.stdin, fieldnames=[
            "order",
            "name",
            "duration",
            "url",
            "artist_name",
            "album_name",
            "album_image",
            "original_tags",
            "published_date",
            "queue_artist",
            "queue_name",
            "lyrics",
            "filtered_tags"
        ])
        
        tracks = []
        for row in reader:
            lyrics = row["lyrics"]
            if lyrics == "Lyrics not found" or lyrics == "API request failed":
                continue
            
            
            sections = list(map(lambda x: { "title": x[0], "content": x[1] }, sections_regex.findall(lyrics)))
            if len(sections) == 0:
                sections = [{ "content": lyrics }]
            
            genres = list(filter(lambda x: x != "", row["filtered_tags"].split("%SEP%")))
            
            duration = int(row["duration"] or "0")
            
            album = {
                "name": row["album_name"],
            }
            
            if row["album_image"] != "":
                album["image"] = row["album_image"]
            
            track = {
                "__order": int(row["order"]),
                "name": row["name"]
            }
            
            if duration > 0:
                track["duration"] = duration
               
                
            if row["url"] != "":
                track["url"] = row["url"]
                
            if row["artist_name"] != "":
                track["artist"] = row["artist_name"]
                
            if row["published_date"] != "":
                track["publishedAt"] = row["published_date"]
                
            if len(sections) > 0:
                track["lyrics"] = sections
                
            if len(genres) > 0:
                track["genres"] = genres
            
            if album["name"] != "":
                track["album"] = album
                
            if duration > 0:
                track["duration"] = duration
                
            tracks.append(track)
                
                
        with open(f"data/tracks.json", "w") as jsonfile:
            json.dump(tracks, jsonfile)
        
        
if __name__ == "__main__":
    main()