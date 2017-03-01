# -*- coding: utf-8 -*-
import os
import sys
import json

import requests
from flask import Flask, request
from bs4 import BeautifulSoup
import validators
from urllib.parse import urlparse

from constants import *
from message import IncomingMessage

app = Flask(__name__)

# valid URLS for searching for things
sources = json.load(open("static/sources.json"))["sources"]
urls_dict = {urlparse(x["url"]).netloc: x["id"] for x in sources}
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

    if request.is_json:
        data = request.get_json()
        if "object" in data.keys():
            handle_query_facebook(data)
        else:
            if "query" in data.keys():
                response = handle_query_default(data['query'])
                return response, 200
    else:
        data = request.get_data()
        response = handle_query_default(data)
        return response, 200

    return "ok", 200

def handle_query_facebook(data):

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]
                    recipient_id = messaging_event["recipient"]["id"]  
                    message_text = messaging_event["message"]["text"]  

                    response = handle_query_default(message_text)
                    send_response_facebook(sender_id, response)

                else:
                    log("handle_facebook_message(): unexpected messagging_event")

def handle_message_text(message_text):

    incoming_message = IncomingMessage(message_text)

    if incoming_message.is_help():
        return ("help", None)
    elif incoming_message.is_sources():
        return ("sources", None)

    elif incoming_message.message_parse_ok:
        
        if incoming_message.source_requested in urls_dict.keys():
            id = urls_dict[incoming_message.source_requested]
        elif incoming_message.source_requested in urls_dict.values():
            id = incoming_message.source_requested
        else:
            url = get_google_search_result(incoming_message.source_requested)
            if url in urls_dict:
                id = urls_dict[url]
            else:
                id = None
        
        if id:
            x = get_headlines_from_source(id, incoming_message.num_requested)   
            return ("ok", x)
        else:
            return ("source_not_found", None)

    else:
        return ("message_parse_failure", None)


def handle_query_default(message_text):
    ''' 
    Constructs a response based on the message
    '''
    result, contents = handle_message_text(query)
    
    if result == "ok":
        response = "\n".join(contents)

    elif result == "source_not_found":
        response = source_not_found_response

    elif result == "help":
        response = welcome_response

    elif result == "sources":
        response = "Sources: " + ", ".join(urls_dict.values())

    elif result == "message_parse_failure":
        response = message_parse_failure_response

    else:
        log("Unexpected response from handle_message_text()")
        response = wrong_response
    
    return response


def send_response_facebook(recipient_id, message_text):

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


def get_google_search_result(search_term):

    '''
    Returns the first 5 search result URLs that are affiliated with a search term
    The strategy is to take the most common url that is not google.com
    that comes back from a google search result of that query.

    Returns:
        - (or None, on failure)
    ''' 

    #slugify the search term 
    concatenated_search_term = search_term.replace(' ', '+')
    search_parameters = {
        "q" : search_term
    }

    r = requests.get(google_search_url, params=search_parameters)
    if r.status_code != 200:
        log("Bad search query")
        log(r.status_code)
        log(r.text)
        return None

    # Get the urls
    soup = BeautifulSoup(r.text, "html.parser")
    urls = soup.findAll("a")
    validated_urls = [urlparse(x['href'].strip("/url?q=")).netloc for x in urls]
    validated_urls_2 = [x for x in validated_urls if "google" not in x and len(x) > 0]
    most_common_url = max(set(validated_urls_2), key=validated_urls_2.count)
    log("{} , {}".format(search_term, most_common_url))

    return most_common_url


def get_headlines_from_source(source, num_requested):
    
    ''' 
    Uses the newspi protocol to get the headlines from that headline
    '''

    params = {
        "source": source, 
        "apiKey" : os.environ["NEWS_API_KEY"], 
        "sortBy" : "top"
    }

    headlines = []

    r = requests.get(newsapi_url, params=params)
    
    if r.status_code == 200:
        for count, news_story in enumerate(r.json()['articles'][:num_requested]):
            response = "{}) {}: {}".format(str(count+1), news_story['title'], news_story['url'])
            headlines.append(response)
        return headlines
    else:
        log(r.status_code)
        log(r.text)
        return None


def log(message): 
    print(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)




