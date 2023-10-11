import os
import json
import re

import lookup_json


with open(os.curdir + "/../data/backup-tracks-with-entities.json", 'r') as f:
    obj = json.load(f)

wc_regex = re.compile(r"\b\S+\b")

def get_words(text):
    yield from map(lambda x: x.group(), wc_regex.finditer(text))

songs = []
for index, lyrics in enumerate(lookup_json.dump(obj, ["*", "lyrics"])):
    sections = list(lookup_json.dump(lyrics, ["*", "content"]))
    
    text = "\n".join(sections)
    num_words = len(list(get_words(text)))
    if num_words != 0:
        songs.append(lookup_json.dump(obj, [str(index)]).__next__())


json.dump(songs, open("../data/final-tracks.json", "w")) 