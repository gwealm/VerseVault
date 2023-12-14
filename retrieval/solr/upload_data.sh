#!/bin/bash

curl -X POST -H 'Content-Type: application/json' 'http://localhost:8983/solr/tracks_initial/update' \
   --data-binary '@./data/tracks.json'

curl -X POST -H 'Content-Type: application/json' 'http://localhost:8983/solr/tracks_refined/update' \
    --data-binary '@./data/tracks.json'

curl -X POST -H 'Content-Type: application/json' 'http://localhost:8983/solr/tracks_semantic/update' \
   --data-binary '@./data/tracks.json'

curl -X POST -H 'Content-Type: application/json' 'http://localhost:8983/solr/tracks_synonyms/update' \
    --data-binary '@./data/tracks.json'