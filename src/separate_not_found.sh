#!/bin/sh

echo "Artist,Track,lyrics" > not_found.csv
grep "Lyrics not found" data/music_data_with_lyrics.csv > not_found.csv

grep -v "Lyrics not found" data/music_data_with_lyrics.csv > data/music_data_with_lyrics_clean.csv
