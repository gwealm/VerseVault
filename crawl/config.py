"""Config file for the crawler."""

import os
from os.path import join, dirname

from dotenv import load_dotenv
load_dotenv()

# Get the API key from the .env file
LASTFM_API_KEY = os.getenv('LASTFM_API_KEY')

# Directory to save the data to
DATA_DIR = join(dirname(__file__), "..", "data")

# Numbers of tracks to get per page of the Top Tracks Chart
TRACKS_NUM = 1000

# Max number of requests per second
RPS = 20
