from flask import Flask, Response, request
from Doc.doc_update import doc_update
import urllib.parse
import json
import requests

app = Flask(__name__)


@app.route("/")
def index():
    return "index"

@app.route("/zoom")
def zoomApp():
    print("call main page3", flush=True)
    return "zoom app home page"

@app.route("/zoomoauth")
def zoomOauth():
    return "zoom oauth"

@app.route("/docUpdate", methods=['POST', 'GET'])
def route_to_doc_update():
    if request.method == 'POST':
        return doc_update(request.form['content'], request.form['link'], request.form['doc_id'])
    return doc_update("Here is the link to your video clip: ", "https://www.youtube.com\n")


# slack slash command's request url
@app.route("/addToDoc", methods=['POST'])
def route_to_add_To_Doc():
    if request.method == 'POST':
        doc_update(request.form['text'])
        return Response(), 200
    return "invalid methods"


@app.route("/slackInteractions", methods=['POST'])
def route_slack_interaction():
    if request.method == 'POST':
        data = request.stream.read().decode("utf-8")
        # print(data, flush=True)
        url_decoded = urllib.parse.unquote(data).split("=")[1]
        decoded_json = json.loads(url_decoded)
        # print(decoded_json, flush=True)
        doc_update(decoded_json["message"]["text"].replace("+"," "))
        return Response(), 200
    return Response(), 200

