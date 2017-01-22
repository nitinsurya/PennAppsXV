from twilio.rest import TwilioRestClient 
 
# put your own credentials here 
account_sid = "AC5915e7510303f274520050035e5994a2" # Your Account SID from www.twilio.com/console
auth_token  = "a2a69b0c42ab9a15e486bc66013d184d"  # Your Auth Token from www.twilio.com/console

 
client = TwilioRestClient(account_sid, auth_token) 
 
client.messages.create(
    from_="+13123131116", 
    to="+13128749015", 
    body="This is the ship that made the Kessel Run in fourteen parsecs?", 
)
