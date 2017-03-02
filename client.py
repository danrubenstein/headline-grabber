#!/usr/local/bin/python3

import requests
import sys

query = " ".join(sys.argv[1:])
headers = {
	'Content-Type' : 'application/json'
}

r = requests.post("https://damp-beach-82114.herokuapp.com/", headers=headers,json={'query':query})

print(r.headers)
print(r.text)
