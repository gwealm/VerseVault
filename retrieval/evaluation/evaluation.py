import matplotlib.pyplot as plt
from sklearn.metrics import PrecisionRecallDisplay
import numpy as np
import json
import requests
import pandas as pd

QRELS_FILE = "qrels/q1.txt"
QUERY_URL = "localhost:5601/tracks/_search"

# Read qrels to extract relevant documents
relevant = list(map(lambda el: el.strip(), open(QRELS_FILE).readlines()))
# Get query results from ElasticSearch instance
results = requests.get(QUERY_URL).json()['response']['docs']