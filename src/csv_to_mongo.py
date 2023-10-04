
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus
import os
from dotenv_vault import load_dotenv
import csv

def write_csv_to_mongo(collection_name):
    with open(f"{collection_name}.csv", newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        collection = client["versevault"][collection_name]
        collection.insert_many(reader)

load_dotenv()
password = os.getenv('PASSWORD')

collections = [
    "track_info",
    "track_queue",
    "album_queue",
    "artist_queue",
    "track_lyrics"
]

if password is not None:
    password = quote_plus(password.encode('utf-8'))

print(password)

URI = f"mongodb+srv://versevault:{password}@cluster.xchibb2.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(URI, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    
    for collection in collections:
        write_csv_to_mongo(collection)
    
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
finally:
    client.close()