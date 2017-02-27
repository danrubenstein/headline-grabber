# -*- coding: utf-8 -*-
import os
import sys
import json

import requests
from flask import Flask, request

from bs4 import BeautifulSoup
from constants import *

from message import IncomingMessage

app = Flask(__name__)

# valid URLS for searching for things
sources = json.load(open("sources.json"))["sources"]
print(sources[1])
urls_dict = {x["url"].split("/")[2]: x["id"] for x in sources}
source_names = [x["name"] for x in sources]

@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    # log(data)  # you may not want to log every incoming message in production, but it's good for testing
    
    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]
                    recipient_id = messaging_event["recipient"]["id"]  
                    message_text = messaging_event["message"]["text"]  

                    incoming_message = IncomingMessage(message_text)

                    if incoming_message.is_help():
                        response = welcome_response
                        send_message(sender_id, response)

                    elif incoming_message.message_parse_ok:
                        
                        pass

                    else:
                        log("!incoming_message.message_parse_ok")

    return "ok", 200


def send_message(recipient_id, message_text):

    try:
        log("sending message to {}: {}".format(recipient_id, message_text))
    except UnicodeEncodeError:
        log("unicode decode error")

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post(facebook_message_api_url, params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(message):  # simple wrapper for logging to stdout on heroku
    print(message)
    sys.stdout.flush()

def get_source(message_text):
    ''' 
    Gets the source based on the urls determined from the message parts. 
    ''' 
    words = message_text.split()

    for word in words:
        url_parts = get_google_search_result(word)
        if url_parts == None:
            pass 
        else:
            for url in url_parts:
                log("{} : {}".format(word, "".join(url)))
                for part in url:
                    for key in urls_dict.keys():
                        if part in key:
                            log("{} : {}".format(part,key))
                            log("returning id: {}".format(urls_dict[key]))
                            return urls_dict[key]

    return None





if __name__ == '__main__':
    app.run(debug=True)



