'''
app.py. Most everything is in here, except message.py
'''
# -*- coding: utf-8 -*-
import os
import sys
import json
from urllib.parse import urlparse

import requests
from flask import Flask, request
from bs4 import BeautifulSoup

from constants import facebook_message_api_url, google_search_url, newsapi_url, welcome_response, wrong_response, source_not_found_response, message_parse_failure_response
from message import IncomingMessage

app = Flask(__name__)
sources = json.load(open("static/sources.json"))["sources"]
CATEGORIES = (list(set([x["category"] for x in sources])))
CATEGORIES_DICT = {x : ", ".join([y["id"] for y in sources if y["category"] == x]) for x in CATEGORIES}

URLS_DICT = {urlparse(x["url"]).netloc: x["id"] for x in sources}
SOURCE_NAMES = [x["name"] for x in sources]

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
                _, response = handle_query_default(data['query'])
                return response, 200
    else:
        data = request.get_data()
        _, response = handle_query_default(data)
        return response, 200

    return "ok", 200

def handle_query_facebook(data):
    '''
    handle_query_facebook is the handler for POST requests 
    that come via the Facebook webhook

    Parameters:
        - data - the body of the POST request (json)

    Returns:
        - None
    '''
    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"] 
                    message_text = messaging_event["message"]["text"]  
                    result, response = handle_query_default(message_text)

                    log("{} {} {}".format(sender_id, message_text, result))
                    if result in ["ok", "sources"]:
                        responses = response.split("\n")
                        for x in responses:
                            send_response_facebook(sender_id, x)
                    else:
                        send_response_facebook(sender_id, response)
                else:
                    pass
                    


def handle_message_text(message_text):
    '''
    handle_message_text takes the query that has been generated against the 
    bot and returns the status and content associated with that query. 

    Args:
        - message_text

    Returns:
        - (result, content)

    Note: if the result is not "ok", content will be None.
    '''

    incoming_message = IncomingMessage(message_text)

    if incoming_message.is_help():
        return ("help", None)
    
    elif incoming_message.is_sources():
        return ("sources", None)

    elif incoming_message.message_parse_ok:
        
        if incoming_message.source_requested in URLS_DICT.keys():
            id = URLS_DICT[incoming_message.source_requested]
        elif incoming_message.source_requested in URLS_DICT.values():
            id = incoming_message.source_requested
        else:
            url = get_google_search_result(incoming_message.source_requested)
            if url in URLS_DICT:
                id = URLS_DICT[url]
            else:
                id = None
        
        if id != None:
            x = get_headlines_from_source(id, incoming_message.num_requested)   
            return ("ok", x)
        else:
            return ("source_not_found", None)

    else:
        return ("message_parse_failure", None)


def handle_query_default(message_text):
    ''' 
    handle_query_default is the standard handler for a message query. Based on 
    the result of handle_message_text, handle_query_default returns a (result, 
    response) tuple that contains either the source-specific response (the 
    headlines) or the appropriate error/utility message. 

    Args:
        - message_text

    Returns
        - (result, response)

    '''
    result, contents = handle_message_text(message_text)
    
    if result == "ok":
        response = "\n".join(contents)

    elif result == "source_not_found":
        response = source_not_found_response

    elif result == "help":
        response = welcome_response

    elif result == "sources":
        response = "Sources: \n" + "\n".join([x + ": " + CATEGORIES_DICT[x] for x in CATEGORIES])

    elif result == "message_parse_failure":
        response = message_parse_failure_response

    else:
        log("Unexpected response from handle_message_text()")
        response = wrong_response
    
    return (result, response)


def send_response_facebook(recipient_id, message_text):
    ''' 
    send_response_facebook sends a POST request to the 
    Facebook API which returns to the user as a chat 
    message.

    Args:
        - recipient_id - the target for the Facebook API
        - message_text

    Returns:
        - The status code of the response
    '''
    # try:
    #     log("sending message to {}: {}".format(recipient_id, message_text))
    # except UnicodeEncodeError:
    #     log("unicode decode error")

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
        log("{}: {}".format(r.status_code, r.text))

    return r.status_code


def get_google_search_result(search_term):
    '''
    If the search query is not recognized by previous checks, 
    get_google_search_result uses the Google Search API to grab the text
    of a search for that term, and that takes the most common domain 
    on that search page.

    Args:
        - search_term

    Returns:
        - most_common_url (None if bad query) 
    ''' 

    concatenated_search_term = search_term.replace(' ', '+')
    search_parameters = {
        "q" : concatenated_search_term
    }

    r = requests.get(google_search_url, params=search_parameters)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)
        return None

    soup = BeautifulSoup(r.text, "html.parser")
    urls = soup.findAll("a")
    validated_urls = [urlparse(x['href'].strip("/url?q=")).netloc for x in urls]
    validated_urls_2 = [x for x in validated_urls if "google" not in x and len(x) > 0]
    most_common_url = max(set(validated_urls_2), key=validated_urls_2.count)

    return most_common_url


def get_headlines_from_source(source, num_requested):
    ''' 
    get_headlines_from_source uses the newspi protocol to get the articles, headlines, and url from that source. 

    Args:
        - source (this must be an accepted newsapi source)
        - num_requested

    Returns:
        - headlines, a list of strings of the form
            "n) <headline>: <article_url>"
    '''
    params = {
        "source" : source, 
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
    '''
    Simple logging function for Heroku logs
    '''
    print(message)
    sys.stdout.flush()


if __name__ == '__main__':
    
    app.run(debug=True)




