#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") == "log.in":
        result = req.get("result")
        parameters = result.get("parameters")
        accinfo = parameters.get("account-info")

        name = {'1111':"Kathryn Janeway", '9999':"James Kirk", '1776':"Jonathan Archer", '1701':"Jean-Luc Picard", '2371':"Benjamin Sisko"}

        speech = "Hello " + str(name[accinfo]) + "! How can I help you today?"

        print("Response:")
        print(speech)

        return {
            "speech": speech,
            "displayText": speech,
            #"data": {},
            "contextOut": [{"name":"logged-in", "lifespan":10, "parameters":{"account-info":accinfo}}],
            "source": "apiai-onlinestore-shipping"
        }
    
    elif req.get("result").get("action") == "check.balance":
        result = req.get("result")
        parameters = result.get("contexts").find("parameters")
        accinfo = parameters.find("account-info")

        balance = {'1111':"$1,000", '9999':"$0.09", '1776':"$99", '1701':"$750", '2371':"$25,000"}

        speech = "Your current balance is " + str(balance[accinfo]) + "."

        print("Response:")
        print(speech)

        return {
            "speech": speech,
            "displayText": speech,
            #"data": {},
            #"contextOut": accinfo,
            "source": "apiai-onlinestore-shipping"
        }


    else:
        return {
            "speech": "I'm sorry, I can not process your request. Please try again!",
            "displayText": speech,
	}


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')
