#!/bin/bash

# Delete cores
curl -X POST "http://localhost:8983/solr/admin/cores?action=UNLOAD&core=tracks_initial&deleteIndex=true&deleteDataDir=true&deleteInstanceDir=true"
curl -X POST "http://localhost:8983/solr/admin/cores?action=UNLOAD&core=tracks_refined&deleteIndex=true&deleteDataDir=true&deleteInstanceDir=true"
curl -X POST "http://localhost:8983/solr/admin/cores?action=UNLOAD&core=tracks_semantic&deleteIndex=true&deleteDataDir=true&deleteInstanceDir=true"
curl -X POST "http://localhost:8983/solr/admin/cores?action=UNLOAD&core=tracks_synonyms&deleteIndex=true&deleteDataDir=true&deleteInstanceDir=true"

# Upload schemas
docker exec -it -u root versevault-solr sh -c "rm -rf /opt/solr/server/solr/configsets/_tracks_semantic && cp -r /data/_tracks_semantic/ /opt/solr/server/solr/configsets/ && chown -R solr:solr /opt/solr/server/solr/configsets/_tracks_semantic"
docker exec -it -u root versevault-solr sh -c "rm -rf /opt/solr/server/solr/configsets/_tracks_synonyms && cp -r /data/_tracks_synonyms/ /opt/solr/server/solr/configsets/ && chown -R solr:solr /opt/solr/server/solr/configsets/_tracks_synonyms"

# Create cores
docker exec -it versevault-solr bin/solr create_core -c tracks_semantic -d _tracks_semantic
docker exec -it versevault-solr bin/solr create_core -c tracks_synonyms -d _tracks_synonyms
