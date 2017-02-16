# -*- coding: utf-8 -*-
import os
import sys
import json

import requests
from flask import Flask, request

from bs4 import BeautifulSoup

app = Flask(__name__)

# valid URLS for searching for things
sources = json.load(open("sources.json"))["sources"]

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

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  # the message's text

                    source = u""

                    ## Various News Outlets

                    source = get_source(message_text)

                    if source != None:

                        params = {
                            "source": source, 
                            "apiKey" : os.environ["NEWS_API_KEY"], 
                            "sortBy" : "top"
                        }

                        response = ""

                        r = requests.get("https://newsapi.org/v1/articles", params=params)
                        
                        if r.status_code == 200:
                            for count, news_story in enumerate(r.json()['articles'][:5]):
                                log(news_story)
                                response = (str(count+1).encode("utf-8") + ") " + (news_story['title']) + ": " + (news_story['url']))
                                send_message(sender_id, response)
                        else:
                            log(r.status_code)
                            log(r.text)
                            send_message(sender_id, "Sorry, there was a problem")

                    elif "help" in message_text.lower():

                        response = "Welcome to Headline Grabber! Get the top news stories from your favorite sites - type one in, or type \"sources\" to see what sources are available \n\n \
                            Powered by newsapi.org"

                        send_message(sender_id, response)

                    elif "sources" in message_text.lower():

                        response = "WSJ"

                        send_message(sender_id, response)
                    else:
                        
                        response = "Sorry, we couldn't find that for you - type \"help\" or \"sources\" to keep going."
                        send_message(sender_id, response)

    

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

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
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
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
                            return urls_dict[key]

    return None


def get_google_search_result(search_term):
    '''
    Allows for one word google searches and returns the first 5 URLs that are 
    found as split parts. 
    ''' 
    search_parameters = {
        "q" : search_term
    }

    search_url = "https://www.google.com/search"

    r = requests.get(search_url, params=search_parameters)

    if r.status_code != 200:
        log("Bad search query")
        log(r.status_code)
        return None

    soup = BeautifulSoup(r.text, "html.parser")
    urls = soup.findAll('cite')[:5]
    url_parts = [x.text.split("/") for x in urls]

    return url_parts

if __name__ == '__main__':
    app.run(debug=True)



