#!/usr/bin/python3

from flask import Flask, request, redirect
import twilio.twiml
from urllib.request import Request, urlopen
import urllib
import json

#ID access to API
TOKEN = "63bab4050efb9bcdf6c436c00e2bc47d" # e.g.: "f03c3c76cc853ee690b879909c9c6f2a"
url = "https://cloudpanel-api.1and1.com/v1"

app = Flask(__name__)

# Try adding your own number to this list!
callers = {
    "+13128749015": "Nitin Surya"
}

@app.route("/", methods=['GET', 'POST'])
def index():
  message = "hello there"
  resp = twilio.twiml.Response()
  resp.message(message)
  
  return str(resp)

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8082, debug=True, threaded=True)
