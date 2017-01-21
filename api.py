#!/usr/bin/python3

from flask import Flask, request, send_from_directory, jsonify, make_response, abort
import os
import requests
from flask_cors import CORS, cross_origin
from collections import Counter
import datetime
import json
import sqlite3

app = Flask(__name__, static_url_path='')
CORS(app)

pennhack_key = "cb3e8a83305f920c21ee1b74e7694bcf"
acc_base_url = "http://api.reimaginebanking.com/accounts/"

conn = sqlite3.connect('trasacts.db')
c = conn.cursor()

@app.route('/')
def root():
  return make_response(jsonify({'text': 'Hello world'}))

@app.route('/sample_text', methods=['GET'])
def sample_text():
  return make_response(jsonify({'text': 'Hello world'}))
 

@app.route('/make_transaction', methods=['GET'])
def make_transaction():
  global acc_base_url
  account_id, out_vals = '57f89267360f81f104543bd1', []
  merchant_id = request.args.get('merchant_id')
  if merchant_id is not None:
    url = acc_base_url + account_id + "/purchases?key=" + pennhack_key
    purchase_details = {"merchant_id": merchant_id, "medium": "balance", "purchase_date": "2017-01-21", "amount": 0.01, "description": "string"}  
    json_data = requests.post(url, data = json.dumps(purchase_details), headers = {'Content-Type': 'application/json'}).json()

    return make_response(jsonify(json_data))
  else:
    jsonify({"error": "Merchant ID not given"}, 404)

def create_action_request():
  pass

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
