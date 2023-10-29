#!/bin/sh

cid=$(docker run -dp 8983:8983 -v ${PWD}:/lyrist solr:9.3)
docker exec -it $cid /bin/bash