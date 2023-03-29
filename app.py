from flask import Flask, request
# from main import chat;
import requests
import json
from config import *
from main import response

app = Flask(__name__)


def graphAPI(sender_id, response):
    payload = {
    'recipient': {'id': sender_id},
    'message': response,
    'messaging_type': 'RESPONSE'
    }
    headers = {'content-type': 'application/json'}


    url = 'https://graph.facebook.com/v14.0/me/messages?access_token={}'.format(PAGE_ACCESS_TOKEN)
    r = requests.post(url, json=payload, headers=headers)
    return 'OK' , 200


def lineMsgAPI(reply_token, reply_message):
    url =  'https://api.line.me/v2/bot/message/reply'
    Authorization = 'Bearer {}'.format(LINE_ACCESS_TOKEN)
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': Authorization
    }
    data = {
        "replyToken": reply_token,
        "messages": [{
            "type": "text",
            "text": str(reply_message)
        }]
    }
    data = json.dumps(data)
    r = requests.post(url, headers=headers, data=data)

    return 'OK' , 200

#function to handle message
def handleFacebookMessage(sender_id, received_message):
    if 'text' in received_message:
        text = received_message['text']
        response_msg = response(text)
        msg_to_send = {"text": str(response_msg) }
        graphAPI(sender_id, msg_to_send)

def handleLineMessage(sender_id, received_message, reply_token):
    if type(received_message) == str:
        response_msg = response(received_message)
        msg_to_send = response_msg
        lineMsgAPI(reply_token, msg_to_send)



@app.route('/', methods=["GET", "POST"])
def home():
    return 'HOME'

#facebook

@app.route('/facebook-webhook', methods=["GET", "POST"])
def Facebook_webhook():
    # verify connection to webhook
    if request.method == 'GET':
        if 'hub.mode' in request.args:
            mode = request.args.get('hub.mode')
        if 'hub.verify_token' in request.args:
            token = request.args.get('hub.verify_token')
        if 'hub.challenge' in request.args:
            challenge = request.args.get('hub.challenge')

        if 'hub.mode' in request.args and 'hub.verify_token' in request.args:
            mode = request.args.get('hub.mode')
            token = request.args.get('hub.verify_token')

            if mode == 'subscribe' and token == VERIFY_TOKEN:
                challenge = request.args.get('hub.challenge')
                return challenge, 200
            else:
                return 'ERROR', 403
        return 'SOMETHING', 200

    # get message
    if request.method == 'POST':
        if 'hub.mode' in request.args:
            mode = request.args.get('hub.mode')
            print(mode)
        if 'hub.verify_token' in request.args:
            token = request.args.get('hub.verify_token')
            print(token)
        if 'hub.challenge' in request.args:
            challenge = request.args.get('hub.challenge')
            print(challenge)

        if 'hub.mode' in request.args and 'hub.verify_token' in request.args:
            mode = request.args.get('hub.mode')
            token = request.args.get('hub.verify_token')

            if mode == 'subscribe' and token == VERIFY_TOKEN:
                print('WEBHOOK VERIFIED')
                challenge = request.args.get('hub.challenge')

                return challenge, 200
            else:
                return 'ERROR', 403

        data = request.data
        body = json.loads(data.decode('utf-8'))
        
        #ดึงข้อมูล
        if 'object' in body and body['object'] == 'page':
            entries = body['entry']
            for entry in entries:
                webhookEvent = entry['messaging'][0]
                # print(webhookEvent)
                sender_id = webhookEvent['sender']['id']

                if 'message' in webhookEvent:
                    handleFacebookMessage(sender_id, webhookEvent['message'])

                return 'EVENT_RECEIVED', 200
        else:
            return 'ERROR', 404



#line

@app.route('/line-webhook', methods=["GET", "POST"])
def line_webhook():
    if request.method == "POST":
        payload = request.json
        event = payload['events'][0]
        if event['type'] == "message":
            # print("webhook line work")
            msg = event['message']['text']
            # print(type(msg))
            sender_id = event['source']['userId']
            reply_token = event['replyToken']
            handleLineMessage(sender_id=sender_id, received_message=msg, reply_token=reply_token)
        return 'OK', 200
    elif request.method == "GET":
        return 'STHELSE' , 201
    else:
        return 'ERROR', 404


