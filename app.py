# import urllib.request
# from bs4 import BeautifulSoup as bs
# from datetime import datetime
# import requests

# # url = "http://www.jeonghyeon.hs.kr/lunch.view?date=" + datetime.today().strftime("%Y%m%d")
# url = "http://www.jeonghyeon.hs.kr/lunch.view?date=20200921"
# html_text = requests.get(url).text

# soup = bs(html_text, "html.parser")
# hh = soup.select('div.menuName>span')
# if not hh:
#     print('정현고 급식 없음')
# else:
#     for hh2 in hh:
#         print(hh2.text)

from flask import Flask, request
import requests
app = Flask(__name__)
FB_API_URL = 'https://graph.facebook.com/v8.0/me/messages'
VERIFY_TOKEN='c914311'
PAGE_ACCESS_TOKEN='EAAFDkuQpZCkABAILlZBKnDZASH9s8QkdEfDZCZB4l967j8p0bUM4uQDZBfEIJDuQ1RqOhiqHp8k4npx2OmBwDyRCO1MYMKOu47OJ7L5TXf4sVHZCh62izYz6SQUUZAER35WCBP33z9UZCgFVlHjZAttZB2BpV9Ei3EZB4QWo9LNJggkpTPwUIciWpZBuo'
def send_message(recipient_id, text):
    """Send a response to Facebook"""
    payload = {
        'message': {
            'text': text
        },
        'recipient': {
            'id': recipient_id
        },
        'notification_type': 'regular'
    }

    auth = {
        'access_token': PAGE_ACCESS_TOKEN
    }

    response = requests.post(
        FB_API_URL,
        params=auth,
        json=payload
    )

    return response.json()

def get_bot_response(message):
    """This is just a dummy function, returning a variation of what
    the user said. Replace this function with one connected to chatbot."""
    return "This is a dummy response to '{}'".format(message)


def verify_webhook(req):
    if req.args.get("hub.verify_token") == VERIFY_TOKEN:
        return req.args.get("hub.challenge")
    else:
        return "incorrect"

def respond(sender, message):
    """Formulate a response to the user and
    pass it on to a function that sends it."""
    response = get_bot_response(message)
    send_message(sender, response)


def is_user_message(message):
    """Check if the message is a message from the user"""
    return (message.get('message') and
            message['message'].get('text') and
            not message['message'].get("is_echo"))


@app.route("/webhook", methods=['GET'])
def listen():
    """This is the main function flask uses to
    listen at the `/webhook` endpoint"""
    if request.method == 'GET':
        return verify_webhook(request)

@app.route("/webhook", methods=['POST'])
def talk():
    payload = request.get_json()
    event = payload['entry'][0]['messaging']
    for x in event:
        if is_user_message(x):
            text = x['message']['text']
            sender_id = x['sender']['id']
            respond(sender_id, text)

    return "ok"

@app.route('/')
def hello():
    return 'hello'

if __name__ == '__main__':
    app.run(threaded=True, port=5000)