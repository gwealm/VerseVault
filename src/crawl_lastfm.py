import time
import pprint
import os
import requests
from dotenv import load_dotenv
import pandas as pd
from typing import Tuple
import csv

import sys

load_dotenv()

# Get the API key from the .env file
LASTFM_API_KEY = os.getenv('LASTFM_API_KEY')

# Directory to save the data
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

# Numbers of tracks to be shown
TRACK_NO = 1000

RPS = 20

def normalize_xml_value(x):
    if isinstance(x, list):
        return x
    
    if isinstance(x, dict):
        return [x]
    
    raise Exception(f"Unknown type {type(x)} for {x}")

# Define the Last.fm API endpoint for chart tracks
# endpoint = f'http://ws.audioscrobbler.com/2.0/?method=chart.gettoptracks&limit={TRACK_NO}&api_key={LASTFM_API_KEY}&format=json'
class DummyCollection:
    def append(self, _x):
        pass
    
def get_csv_path(filename):
    return os.path.join(DATA_DIR, filename)
    
def tee_to_csv(array, filename, cols):
    
    file_handle = open(get_csv_path(filename), 'a')
    csv_writer = csv.writer(file_handle, quoting=csv.QUOTE_NONNUMERIC)
    
    def add_to_array(x):
        array.append(x)
        
        if isinstance(x, dict):
            csv_writer.writerow([x[col] for col in cols])
        else:
            csv_writer.writerow(x)
        
    return (array, add_to_array)


last_request = 0

def get_from_lastfm(method: str, **kwargs) -> dict | None:
    global last_request

    while True:
        now = time.time()
        if now - last_request > 1 / RPS:
            break
        
        time.sleep(1 / RPS - (now - last_request))
        
    last_request = time.time()
    
    kwargs['api_key'] = LASTFM_API_KEY
    kwargs['format'] = 'json'
    kwargs['method'] = method
    
    while True:
        try:
            response = requests.get(f'https://ws.audioscrobbler.com/2.0/', params=kwargs)
            
            if not response.ok:
                print(f"Request not ok with status code {response.status_code} on URL \"{response.url}\"\n{response.text}\n", file=sys.stderr)
                return None
    
            return response.json()

        except InterruptedError:
            sys.exit(1)
        except Exception as e:
            print(f"Request caused exception {e} on params \"{kwargs}\"\n", file=sys.stderr)
            time.sleep(5)
        


Track = Tuple[str, str]

(_, write_track_info) = tee_to_csv(DummyCollection(), 'track_info.csv', [
    "name",
    "duration",
    "url",
    "artist_name",
    "album_name",
    "album_image",
    "tags",
    "published_date",
    "queue_artist",
    "queue_name"
])

seen_tracks = set()
(track_queue, add_to_track_queue) = tee_to_csv([], 'track_queue.csv', ["artist_name", "track_name"])

seen_albums = set()
(album_queue, add_to_album_queue) = tee_to_csv([], 'album_queue.csv', ["artist_name", "album_name"])
(_, mark_album_as_visited) = tee_to_csv(DummyCollection(), "album_visited.csv", ["artist_name", "album_name"])

seen_artists = set()
(artist_queue, add_to_artist_queue) = tee_to_csv([], 'artist_queue.csv', ["artist_name"])
(_, mark_artist_as_visited) = tee_to_csv(DummyCollection(), "artist_visited.csv", ["artist_name"])


def restore_progress():
    with open(get_csv_path('track_queue.csv'), 'r') as csv_file:
        tracks = [tuple(track) for track in csv.reader(csv_file)]
        seen_tracks.update(tracks)
        track_queue.extend(tracks)
        
    with open(get_csv_path('track_info.csv'), 'r') as csv_file:
        visited_tracks = [(track[8], track[9]) for track in csv.reader(csv_file)]
        for track in visited_tracks:
            try:
                track_queue.remove(track)
            except:
                pass
            
    with open(get_csv_path('album_queue.csv'), 'r') as csv_file:
        albums = [tuple(album) for album in csv.reader(csv_file)]
        seen_albums.update(albums)
        album_queue.extend(albums)
        
    with open(get_csv_path('album_visited.csv'), 'r') as csv_file:
        visited_albums = [tuple(album) for album in csv.reader(csv_file)]
        for album in visited_albums:
            try:
                album_queue.remove(album)
            except:
                pass
        
    with open(get_csv_path('artist_queue.csv'), 'r') as csv_file:
        artists = [tuple(artist) for artist in csv.reader(csv_file)]
        seen_artists.update(artists)
        artist_queue.extend(artists)
        
    with open(get_csv_path('artist_visited.csv'), 'r') as csv_file:
        visited_artists = [tuple(artist) for artist in csv.reader(csv_file)]
        for artist in visited_artists:
            try:
                artist_queue.remove(artist)
            except:
                pass
        
    

def schedule_track_visit(track: Track):
    if track in seen_tracks:
        return
    
    seen_tracks.add(track)
    add_to_track_queue(track)
    
def schedule_album_visit(album: Tuple[str, str]):
    if album in seen_albums:
        return
    
    seen_albums.add(album)
    add_to_album_queue(album)
    
def schedule_artist_visit(artist: str):
    if artist in seen_artists:
        return
    
    seen_artists.add((artist, ))
    add_to_artist_queue((artist,))

def visit_album(album):
    album_artist_name, album_title = album
    res = get_from_lastfm('album.getInfo', artist=album_artist_name, album=album_title)
    
    if res is None:
        mark_album_as_visited(album)
        return
    
    schedule_artist_visit(album_artist_name)
    
    if "tracks" in res["album"]:
        album_tracks = normalize_xml_value(res["album"]["tracks"]["track"])
        
        for track in album_tracks:
            track_tuple = (track["artist"]["name"], track["name"])
            schedule_track_visit(track_tuple)
            
    mark_album_as_visited(album)
        
            
def visit_artist(artist_tuple: Tuple[str]):
    artist, = artist_tuple
    
    res = get_from_lastfm('artist.getTopTracks', artist=artist)
    
    if res is not None:
        top_tracks = normalize_xml_value(res["toptracks"]["track"])
        
        for top_track in top_tracks:
            track_tuple = (top_track["artist"]["name"], top_track["name"])
            schedule_track_visit(track_tuple)
        
    res = get_from_lastfm('artist.getTopAlbums', artist=artist)
    
    if res is not None:
        top_albums = normalize_xml_value(res["topalbums"]["album"])
    
        for top_album in top_albums:
            album_tuple = (top_album["artist"]["name"], top_album["name"])
            schedule_album_visit(album_tuple)
    
    res = get_from_lastfm('artist.getSimilar', artist=artist)
    
    if res is not None:
        similar_artists = normalize_xml_value(res["similarartists"]["artist"])
    
        for similar_artist in similar_artists:
            schedule_artist_visit(similar_artist["name"])
            
    mark_artist_as_visited(artist_tuple)
               
    
def visit_track(track: Track):
    artist, track_name = track
    res = get_from_lastfm('track.getInfo', artist=artist, track=track_name)
    
    if res is None:
        return
    
    if "track" not in res:
        relevant_track_data = {
            "name": None,
            "duration": None,
            "url": None,
            "artist_name": None,
            "album_name": None,
            "album_image": None,
            "tags": None,
            "published_date": None,
            "queue_artist": artist,
            "queue_name": track_name
        }
        
        schedule_artist_visit(artist)
    else:
        track_info = res["track"]
        
        relevant_track_data = {
            "name": track_info["name"],
            "duration": track_info["duration"],
            "url": track_info["url"],
            "artist_name": track_info["artist"]["name"],
            "album_name": None,
            "album_image": None,
            "tags": None,
            "published_date": None,
            "queue_artist": artist,
            "queue_name": track_name
        }
        
        if "album" in track_info:
            
            album_artist_name = track_info["album"]["artist"]
            album_title = track_info["album"]["title"]
            schedule_album_visit((album_artist_name, album_title))
                
            relevant_track_data["album_name"] = album_title
            
            if "image" in track_info["album"] and len(track_info["album"]["image"]) > 0:
                relevant_track_data["album_image"] = track_info["album"]["image"][-1]["#text"]
                
        if "toptags" in track_info and "tag" in track_info["toptags"]:
            relevant_track_data["tags"] = "%SEP%".join([tag["name"] for tag in normalize_xml_value(track_info["toptags"]["tag"])])
            
        if "wiki" in track_info and "published" in track_info["wiki"]:
            relevant_track_data["published_date"] = track_info["wiki"]["published"]
            
        artist_name = track_info["artist"]["name"]
        schedule_artist_visit(artist_name)
        
    write_track_info(relevant_track_data)
        
def main():
    
    restore_progress()

    artist_page = 1
    while True:
        res = get_from_lastfm('chart.getTopArtists', page=artist_page, limit=1000)
        if res is None:
            continue
        
        artist_chart_page = normalize_xml_value(res["artists"]["artist"])
        
        if len(artist_chart_page) == 0:
            break
        
        for artist in artist_chart_page:
            schedule_artist_visit(artist["name"])
            
        artist_page += 1
            
    track_page = 1
    while True:
        res = get_from_lastfm('chart.getTopTracks', page=track_page, limit=1000)
        
        if res is None:
            continue
        
        track_chart_page = normalize_xml_value(res["tracks"]["track"])
        
        if len(track_chart_page) == 0:
            break
        
        for track in track_chart_page:
            schedule_track_visit((track["artist"]["name"], track["name"]))
            
        track_page += 1
        
    while True:
        
        if len(track_queue) > 0:
            next_track = track_queue.pop(0)
            print(f"Visiting track {next_track}")
            visit_track(next_track)
            
        elif len(album_queue) > 0:
            next_album = album_queue.pop(0)
            print(f"Visiting album {next_album}")
            visit_album(next_album)
            
        elif len(artist_queue) > 0:
            next_artist = artist_queue.pop(0)
            print(f"Visiting artist {next_artist}")
            visit_artist(next_artist)
            
        else:
            break
        
    print("Done!")
    
if __name__ == '__main__':
    main()