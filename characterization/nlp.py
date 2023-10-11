import os
import json
import re
import lookup_json
import pandas as pd
import spacy
import csv
from spacy import displacy

nlp = spacy.load('en_core_web_sm')

DATA_DIR = "./data/"


def process_text(text):
    doc = nlp(text)
    sentences = list(doc.sents)
    # Do additional processing if needed
    return sentences

if __name__ == '__main__':
    with open(os.curdir + "/../data/backup-tracks.json", 'r') as f:
        obj = json.load(f)

    for index, lyrics in enumerate(lookup_json.dump(obj, ["*", "lyrics"])):
        text = " ".join(lookup_json.dump(lyrics, ["*", "content"]))
        
        doc = nlp(text)

        sentences = list(doc.sents)
        # print(sentences)\

        # tokenization
        # for token in doc:
            # print(token.text)

        # entities
        ents = [{ "text": e.text, "start": e.start_char, "end": e.end_char, "type": e.label_} for e in doc.ents]
        # print(ents)

        displacy.render(doc, style='ent')
        
        track = next(lookup_json.dump(obj, [str(index)]))
        track["entities"] = ents
        print(f'Status: {(index / len(obj)) * 100}% Completed')
        
    json.dump(obj, open("data/backup-tracks-with-entities.json", "w")) 
        
        
        