
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId
from urllib.parse import quote_plus
import os
from dotenv import load_dotenv
import json

class MyJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return json.JSONEncoder.default(self, obj)
    
def write_mongo_to_json():
    with open(f"data/backup-tracks.json", "w") as jsonfile:
        collection = client["versevault"]["tracks"]
        
        tracks = list(collection.find({}))
        json.dump(tracks, jsonfile, cls=MyJSONEncoder)

load_dotenv()
password = os.getenv('PASSWORD')

if password is not None:
    password = quote_plus(password.encode('utf-8'))

print(password)

URI = f"mongodb+srv://versevault:{password}@cluster.xchibb2.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(URI, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    
    write_mongo_to_json()
    
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
finally:
    client.close()