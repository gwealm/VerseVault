from flask import Flask


app = Flask(__name__)

@app.route("/")
def query():
    headers = {"Content-Type": "application/json"}

    return ({"res": "loladinha"}, headers)