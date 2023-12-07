from flask import Flask
from flask import request

import requests
from sentence_transformers import SentenceTransformer

"""
run flask run in the /api directory to start the api server
"""

app = Flask(__name__)

@app.route("/")
def query():
    solr_endpoint = "http://localhost:8983/solr"
    collection = "tracks_refined"

    query_string = request.args.get('q')

    embedding = text_to_embedding(query_string)

    try:
        results = solr_knn_query(solr_endpoint, collection, embedding)
        print(results)
        return results
    except requests.HTTPError as e:
        print(f"Error {e.response.status_code}: {e.response.text}")
        return {"error": "failed to get results"}


def text_to_embedding(text):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embedding = model.encode(text, convert_to_tensor=False).tolist()
    
    # Convert the embedding to the expected format
    embedding_str = "[" + ",".join(map(str, embedding)) + "]"
    return embedding_str

def solr_knn_query(endpoint, collection, embedding):
    url = f"{endpoint}/{collection}/select"

    data = {
        "q": f"{{!knn f=content_vector topK=10}}{embedding}",
        "fl": "id,lyrics,content,name,artist,[child],score",
        "rows": 10,
        "wt": "json"
    }
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    response = requests.post(url, data=data, headers=headers)
    response.raise_for_status()
    return response.json()
