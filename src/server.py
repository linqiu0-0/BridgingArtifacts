from flask import Flask
from doc_update import doc_update
from flask import request

app = Flask(__name__)

@app.route("/")
def index():
    return "index"

@app.route("/DocUpdate", methods=['POST', 'GET'])
def route_to_doc_update():
    if request.method == 'POST':
        return doc_update(request.form['content'], request.form['link'], request.form['doc_id'])
    return doc_update("Here is the link to your video clip: ", "https://www.youtube.com\n")