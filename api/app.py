from flask import Flask
from flask import request
from flask_cors import CORS

import requests
from sentence_transformers import SentenceTransformer

"""
run flask run in the /api directory to start the api server
"""

app = Flask(__name__)
CORS(app)

@app.route("/<collection>")
def query(collection: str):
    print(f"{collection}")
    solr_endpoint = "http://localhost:8983/solr"

    query = request.args.get('q')

    try:
        if collection == "tracks_semantic":
            query = text_to_embedding(query)
            results = solr_knn_query(solr_endpoint, collection, query)
        else:
            results = solr_query(solr_endpoint, collection, query)
        
        print(results)
        return results
    except requests.HTTPError as e:
        print(f"Error {e.response.status_code}: {e.response.text}")
        return {"error": "failed to get results"}

def solr_query(endpoint, collection, query):
    url = f"{endpoint}/{collection}/select"

    data = {
        "q": f"{{!parent which=doc_type:track filters=$childfq score=total}}{{!edismax qf=\"title^0.5 content^4 content_phonetic^2\" pf=\"content^10\"}}({query})~3",
        "fl": "id,name,artist,score,album.image,genres",
        "sort": "score desc",
        "rows": 20,
        "wt": "json"
    }
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    response = requests.post(url, data=data, headers=headers)
    response.raise_for_status()
    return response.json()

def text_to_embedding(text):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embedding = model.encode(text, convert_to_tensor=False).tolist()
    
    # Convert the embedding to the expected format
    embedding_str = "[" + ",".join(map(str, embedding)) + "]"
    return embedding_str

def solr_knn_query(endpoint, collection, embedding):
    url = f"{endpoint}/{collection}/select"

    data = {
        "q": f"{{!knn f=content_vector topK=20}}{embedding}",
        "fl": "id,name,artist,score,album.image,genres",
        "sort":"score desc",
        "rows": 20,
        "wt": "json"
    }
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    response = requests.post(url, data=data, headers=headers)
    response.raise_for_status()
    return response.json()

@app.route("/cores")
def get_cores():
    url = "http://localhost:8983/api/cores"

    response = requests.get(url)
    response.raise_for_status()
    return response.json()

@app.route("/<collection>/tracks/<track_name>")
def track(collection: str, track_name: str):
    
    url = f"http://localhost:8983/solr/{collection}/select"

    data = {
        "q": f"id:{track_name}",
        "fl": "*,[child]",
        "rows": 20,
        "wt": "json"
    }
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    response = requests.post(url, data=data, headers=headers)
    response.raise_for_status()
    return response.json()
