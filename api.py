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

sqlite3.connect(":memory:", check_same_thread=False)
conn = sqlite3.connect('trasacts.db')
c = conn.cursor()

@app.route('/')
def root():
  return make_response(jsonify({'text': 'Hello world'}))

@app.route('/sample_text', methods=['GET'])
def sample_text():
  return make_response(jsonify({'text': 'Hello world'}))

@app.route('/create_action', methods=['POST'])
def create_action():
  global acc_base_url, c, conn
  account_id = '57f89267360f81f104543bd1'
  data = request.get_json()
  c.execute("insert into transactions(`name`, `product_id`, `product_name`, `product_imgurl`, `merchant_id`, `merchant_name`, `date_time`, `product_desc`, `amount`) values (?,?,?,?,?,?,?,?,?)", data['name'], data['pid'], data['pname'], data['img'], data['mid'], data['mname'], data['date'], data['pdesc'], data['amount'])
  conn.commit()
  return make_response(jsonify({}))

@app.route('/pending_req', methods=['GET'])
def pending_req():
  conn,c=create_connec()
  c.execute("select * from transactions")
  #print(c.fetchall(),file=sys.stderr)
  return make_response(jsonify(c.fetchall()))

@app.route('/make_transaction', methods=['GET'])
def make_transaction():
  global acc_base_url
  account_id, out_vals = '57f89267360f81f104543bd1', []
  merchant_id = request.args.get('merchant_id')
  action_id = request.args.get('transaction_id')
  if merchant_id is not None:
    url = acc_base_url + account_id + "/purchases?key=" + pennhack_key
    purchase_details = {"merchant_id": merchant_id, "medium": "balance", "purchase_date": "2017-01-21", "amount": 0.01, "description": "string"}  
    json_data = requests.post(url, data = json.dumps(purchase_details), headers = {'Content-Type': 'application/json'}).json()
    #update_action_row(action_id, json_data, account_id)

    return make_response(jsonify(json_data))
  else:
    return make_response(jsonify({"error": "Merchant ID not given"}, 404))

def update_action_row(action_id, co_transaction_id, payer_id):
  global c, conn
  c.execute("update transactions set transaction_id = '?' and approver_id = '?' where id = ?", co_transaction_id, payer_id, action_id)
  conn.commit()

def create_connec():
  conn = sqlite3.connect('trasacts.db')
  c = conn.cursor()
  return conn,c
  

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
