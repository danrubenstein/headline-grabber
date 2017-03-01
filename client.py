#!/usr/local/bin/python3

import requests
import sys

query = " ".join(sys.argv[1:])
headers = {
	'Content-Type' : 'application/json'
}
r = requests.post("http://0.0.0.0:5000", headers=headers, json={'query':query})
r = requests.post("https://calm-wave-49418.herokuapp.com/", headers=headers,json={'query':query})

print(r.text)
