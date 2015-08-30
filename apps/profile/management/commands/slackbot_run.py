from apps.profile.slack import slackbot
import time
import os
import sys
import logging
from slackclient import SlackClient

token = os.environ["DATABOT"]
sc = SlackClient(token)
if sc.rtm_connect():
    while True:
        data = sc.rtm_read()
        if len(data) > 0:
            try:
                mtype = data[0]['type']
            except KeyError:
                pass
            else:
                if mtype == 'message':
                    if ":" in data[0]['text'] or "User" in data[0]['text']:
                        response = slackbot(data)
                        sc.rtm_send_message('stats', response)
        time.sleep(1)
