#!/usr/bin/python3

from flask import Flask, request, send_from_directory, jsonify, make_response, abort
import os
import requests
from flask_cors import CORS, cross_origin
from collections import Counter
import datetime
import json
import sqlite3
import sys
from twilio.rest import TwilioRestClient 

app = Flask(__name__, static_url_path='')
CORS(app)

pennhack_key = "cb3e8a83305f920c21ee1b74e7694bcf"
acc_base_url = "http://api.reimaginebanking.com/accounts/"

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/sample_text', methods=['GET'])
def sample_text():
  return make_response(jsonify({'text': 'Hello world'}))

@app.route('/create_action', methods=['POST'])
def create_action():
  global acc_base_url
  conn, c = create_connec()
  account_id = '57f89267360f81f104543bd1'
  data = json.loads(list(request.form.keys())[0])['data']
  c.execute("insert into transactions(`name`, `product_id`, `product_name`, `product_imgurl`, `merchant_id`, `merchant_name`, `date_time`, `product_desc`, `amount_new`, `comment`) values (?,?,?,?,?,?,?,?,?,?)", [data['name'], data['pid'], data['pname'], data['img'], data['mid'], data['mname'], data['date'], data['pdesc'], data['amount'], data['comment']])
  conn.commit()
  c.close()
  return make_response(jsonify({}))

@app.route('/get_balance_details', methods=['GET'])
def get_balance_details():
  url = "http://api.reimaginebanking.com/accounts/57f89267360f81f104543bd1?key=cb3e8a83305f920c21ee1b74e7694bcf"
  reviewer_balance = requests.get(url).json()['balance']
  requester_balance = 200
  conn, c = create_connec()
  c.execute("select sum(amount) from transactions where transaction_id is not null and transaction_id != 0;")
  requester_spent = list(c.fetchone())[0]
  if requester_spent:
    requester_spent = int(requester_spent)
  else:
    requester_spent = 0
  c.close()
  return make_response(jsonify({'requester_balance': requester_balance, 'requester_spent': requester_spent, 'reviewer_balance': reviewer_balance}))

@app.route('/pending_req', methods=['GET'])
def pending_req():
  conn,c = create_connec()
  c.execute("select * from transactions where transaction_id is null")
  res = get_fetchall_res(c.fetchall())
  c.close()
  conn.close()
  return make_response(jsonify(res))

@app.route('/actions_history', methods=['GET'])
def actions_history():
  conn,c = create_connec()
  account_id, out_vals = '57f89267360f81f104543bd1', []
  c.execute("select * from transactions where approver_id = '"+ account_id + "'")
  res = get_fetchall_res(c.fetchall())
  c.close()
  conn.close()
  return make_response(jsonify(res))

@app.route('/make_transaction', methods=['POST'])
def make_transaction():
  global acc_base_url, pennhack_key
  account_id, out_vals = '57f89267360f81f104543bd1', []
  data = json.loads(list(request.form.keys())[0])
  merchant_id = data['merchant_id']
  action_id = data['transaction_id']
  if merchant_id is not None:
    if data['decision'] == 0:
      json_data = {}
      co_transaction_id = '0'
      send_approval_reject_sms(0)
    else:
      url = acc_base_url + account_id + "/purchases?key=" + pennhack_key
      purchase_details = {"merchant_id": merchant_id, "medium": "balance", "purchase_date": data['purchase_data'], "amount": data['amount'], "description": data['pdesc']}  
      json_data = requests.post(url, data = json.dumps(purchase_details), headers = {'Content-Type': 'application/json'}).json()
      co_transaction_id = json_data['objectCreated']['_id']
      send_approval_reject_sms(1)
    update_action_row(action_id, co_transaction_id, account_id)

    return make_response(jsonify(json_data))
  else:
    return make_response(jsonify({"error": "Merchant ID not given"}, 404))

def update_action_row(action_id, co_transaction_id, payer_id):
  conn, c = create_connec()
  c.execute("update transactions set transaction_id = '{a}',  approver_id = '{b}' where id = {c}".format(a=co_transaction_id, b=payer_id, c=action_id))
  conn.commit()
  c.close()

def create_connec():
  conn = sqlite3.connect('transacts.db')
  conn.row_factory = sqlite3.Row
  c = conn.cursor()
  return conn,c

def get_fetchall_res(res):
  if res:
    res = [dict(x) for x in list(res)]
  else:
    res = []
  return res

def send_approval_reject_sms(state):
  # put your own credentials here 
  account_sid = "AC5915e7510303f274520050035e5994a2" # Your Account SID from www.twilio.com/console
  auth_token  = "a2a69b0c42ab9a15e486bc66013d184d"  # Your Auth Token from www.twilio.com/console
  client = TwilioRestClient(account_sid, auth_token) 

  if state:
    body = "Your transaction request approved."
  else:
    body = "Your transaction request rejected."
   
  client.messages.create(
      from_="+13123131116", 
      to="+13128749015", 
      body=body, 
  )
   
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
