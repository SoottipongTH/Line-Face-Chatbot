from flask import Flask, request
import requests
import json

app = Flask(__name__)

PAGE_ACCESS_TOKEN = "EAATYxoah5sYBACd565BPMPywDjaw5D2hQSZBwTYsC69qb4LvWWFKgBrP8VfsRhBffZC6WCgqXeiGeNkkNKyjjK6klvamxGLXLfY8pyVb5XaqXEqKbQKiJmsw4fibDyr6l2pYbNQkpe2XNTJG2RNZAMsGfaf7qRXmGsBwAqPKeuC6wTqIjpR"
VERIFY_TOKEN = "chatbotfacebook"

def graphAPI(senderPsid, response):
    # รับส่ง payload
    payload = {
    'recipient': {'id': senderPsid},
    'message': response,
    'messaging_type': 'RESPONSE'
    }
    headers = {'content-type': 'application/json'}
    #เชื่อมกับ facebook graphapi
    url = 'https://graph.facebook.com/v14.0/me/messages?access_token={}'.format(PAGE_ACCESS_TOKEN)
    r = requests.post(url, json=payload, headers=headers)
    print(r.text)



#func to handle
def handleMessage(senderPsid, receivedMessage):
    #ดูว่ารับ text มารึปล่าว
    print('We entered the HANDLE MESSAGE FUNCTION')
    if 'text' in receivedMessage:
        print('TEXT does exist in the RECEIVER MESSAGE')
        toSend = receivedMessage['text']
        response = {"text": toSend }
        graphAPI(senderPsid, response)
    else:
        response = {"text": 'This chatbot only accepts text messages'}
        graphAPI(senderPsid, response)




@app.route('/', methods=["GET", "POST"])
def home():
    return 'HOME'


@app.route('/webhook', methods=["GET", "POST"])
def index():
    if request.method == 'GET':
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

        return 'SOMETHING', 200


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
                print(webhookEvent)

                senderPsid = webhookEvent['sender']['id']
                print('Sender PSID: {}'.format(senderPsid))

                if 'message' in webhookEvent:
                    handleMessage(senderPsid, webhookEvent['message'])

                return 'EVENT_RECEIVED', 200
        else:
            return 'ERROR', 404
        
        
if __name__ == '__main__':
    debug=True
    app.run()