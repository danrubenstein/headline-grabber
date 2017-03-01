'''
constants.py contains a lot of constants, categorized for easy use. 
'''

# Response Constants
welcome_response = "Welcome to Headline Grabber! Get the top news stories from your favorite sites - type one in, or type \"sources\" to see what sources are available \n\nPowered by newsapi.org"
wrong_response = "Sorry, something went wrong."
source_not_found_response = "Sorry, we couldn't find that for you - type \"help\" or \"sources\" to keep going."
message_parse_failure_response = "Please use the following syntax: <sort_by><count_headlines><source>"

# API URL constants
facebook_message_api_url = "https://graph.facebook.com/v2.6/me/messages"
google_search_url = "https://www.google.com/search"
newsapi_url = "https://newsapi.org/v1/articles"

# Regex Constants
message_full_regex = "(top|latest)\ [0-9]+\ [\ a-z0-9]+"
message_default_regex = "[\ a-z0-9]+"