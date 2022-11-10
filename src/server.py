from datetime import datetime

from flask import Flask, Response, request
import urllib.parse
import json
from flask_cors import CORS
import requests

from Doc.doc_update import doc_update
from Doc.doc_add_meeting_header import add_meeting_header
from Doc.replace_name_range import replace_named_range, delete_name_range


app = Flask(__name__)
cors = CORS(app)

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
@app.route("/slack/addToDoc", methods=['POST'])
def route_to_add_To_Doc():
    if request.method == 'POST':
        # build the text

        now = datetime.now()
        # dd/mm/YY H:M:S
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        text = request.form['text'] + "  [added by " + request.form['user_name'] + " on "+ dt_string+ "]"
        replace_named_range("pre_name_range", text)
        return Response(), 200
    return "invalid methods"


@app.route("/slack/addNextMeeting", methods=['POST'])
def route_to_add_next_meeting():
    if request.method == 'POST':
        delete_name_range("pre_name_range")
        delete_name_range("post_name_range")

        res = add_meeting_header(request.form['text'])
        if res == "200":
            return Response(), 200
        else :
            return Response(), res

    return "invalid methods"


@app.route("/slackInteractions", methods=['POST'])
def route_slack_interaction():
    if request.method == 'POST':
        data = request.stream.read().decode("utf-8")
        # print(data, flush=True)
        url_decoded = urllib.parse.unquote(data).split("=")[1]
        decoded_json = json.loads(url_decoded)
        print(decoded_json, flush=True)

        now = datetime.now()
        # dd/mm/YY H:M:S
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        text = decoded_json["message"]["text"].replace("+", " ") + "  [added by " + decoded_json["user"]["name"] + " on "+ dt_string+ "] "
        replace_named_range("pre_name_range", text)
        return Response(), 200
    return Response(), 200


@app.route("/zoomstart", methods=['POST'])
def zoomStart():
    if request.method == 'POST':
        data = request.stream.read().decode("utf-8")
        print(data, flush=True)
        return Response(), 200
