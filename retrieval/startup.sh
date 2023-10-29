#!/bin/bash

usage() {
    echo "Usage: $0 [-s <schema_file>] [-d <data_file>]"
    echo "Optional: -s <schema_file> Specify the schema file (default: schema1.json)"
    echo "          -d <data_file> Specify the data file (default: backup-tracks.json)"
    echo "          -c <core_name> Specify the name for the core initially created (default: tracks)"
    exit 1
}

schema_file="schema1.json"
data_file="backup-tracks-with-entities.json"
core_name="tracks"

while getopts "s:d:c:" opt; do
    case $opt in
        s) schema_file=$OPTARG;;
        d) data_file=$OPTARG;;
        c) core_name=$OPTARG;;
        *) usage;;
    esac
done

# precreate-co tracks

# Start Solr in background mode so we can use the API to upload the schema
# solr start
/opt/solr/bin/solr create_core -c tracks -V

# Schema definition via API
curl -X POST -H 'Content-type:application/json' \
    --data-binary @"./$schema_file" \
    "http://localhost:8983/solr/$core_name/schema"

# Populate collection
/opt/solr/bin/post -c $core_name ../data/"$data_file"

# Restart in foreground mode so we can access the interface
solr restart -f
