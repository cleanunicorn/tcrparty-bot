#!/usr/bin/env python3
import twitter
import json
import time
import re

print("Start")

tokens = {}
with open("tokens.json") as f:
    tokens = f.read()
    tokens = json.loads(tokens)

api = twitter.Api(
    consumer_key=tokens["consumer_key"],
    consumer_secret=tokens["consumer_secret"],
    access_token_key=tokens["access_token_key"],
    access_token_secret=tokens["access_token_secret"],
)

print(api.VerifyCredentials() is not None)

retry_sleep = ("10", "seconds")
while True:
    # Get the latest message id
    print("Getting direct messages")
    dms = api.GetDirectMessages(skip_status=True, full_text=True, return_json=True)
    last_dm = dms["events"][0]
    last_dm_id = last_dm["id"]

    # Request tokens from faucet
    print("Sending 'faucet' to tcrpartyvip")
    dm = api.PostDirectMessage("faucet", screen_name="tcrpartyvip", return_json=True)
    time.sleep(5) # Wait a few seconds for the reply

    # Wait for message confirmation
    replied = False
    confirmed = False
    retry = False
    while replied == False:
        dms = api.GetDirectMessages(
            since_id=last_dm_id, skip_status=True, full_text=True, return_json=True
        )
        for dm in dms["events"]:
            if dm["message_create"]["sender_id"] == "1029028522843627520":
                replied = True
                message_text = dm["message_create"]["message_data"]["text"]
                print("Found reply: {}".format(message_text))
                if message_text.find("You got it.") != -1:
                    confirmed = True
                    retry_sleep = ('24', 'hours')
                    print("Received tokens")

                regex_match_time = (
                    r"Try again ([0-9]+) (hours|minutes|seconds) from now."
                )
                matches = re.search(regex_match_time, message_text)
                if matches is not None:
                    retry = True
                    retry_sleep = matches.groups()
                    print("Too early to get tokens")
                
                break

    print("Sleeping {} {}".format(retry_sleep[0], retry_sleep[1]))
    if retry_sleep[1] == "minutes":
        time.sleep(int(retry_sleep[0]) * 60)
    elif retry_sleep[1] == "hours":
        time.sleep(int(retry_sleep[0]) * 3600)
    elif retry_sleep[1] == "seconds":
        time.sleep(int(retry_sleep[0]))
