
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus
import os
from dotenv import load_dotenv
import json

def remove_id_from_dict(x: dict):
    x.pop("_id")
    return x    

def write_json_to_mongo():
    with open(f"data/backup-tracks-with-entities.json", "r") as jsonfile:
        tracks = json.load(jsonfile)
        collection = client["versevault"]["tracks"]
        
        collection.delete_many({})    
        collection.insert_many(map(remove_id_from_dict, tracks))

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
    
    write_json_to_mongo()
    
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
finally:
    client.close()