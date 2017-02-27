''' 
This file handles external API calls
''' 
import requests
from constants import *
from bs4 import BeautifulSoup

def get_google_search_result(search_term):

    '''
    Returns the first 5 search result URLs that are affiliated with a search term

    Returns:
        - (or None, on failure)
    ''' 

    concatenated_search_term = search_term.replace(' ', '+')
    search_parameters = {
        "q" : search_term
    }

    print('2')
    r = requests.get(google_search_url, params=search_parameters)
    print('3')
    if r.status_code != 200:
        log("Bad search query")
        log(r.status_code)
        log(r.text)
        return None

    soup = BeautifulSoup(r.text, "html.parser")
    print(r.text)
    urls = soup.findAll('cite')[:5]

    return urls

def get_headlines_from_source(source):
    
    ''' 
    Uses the newspi protocol to get the headlines from that headline
    '''

    params = {
        "source": source, 
        "apiKey" : os.environ["NEWS_API_KEY"], 
        "sortBy" : "top"
    }

    headlines = []

    r = requests.get("https://newsapi.org/v1/articles", params=params)
    
    if r.status_code == 200:
        for count, news_story in enumerate(r.json()['articles'][:5]):
            response = (str(count+1).encode("utf-8") + ") "
                + (news_story['title']) + ": " 
                + (news_story['url']))
            headlines.append(response)
        return headlines
    else:
        log(r.status_code)
        log(r.text)
        return None
        