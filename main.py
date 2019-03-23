#!/usr/bin/env python3
import twitter
import json
import time

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

print(api.VerifyCredentials())

def fibonacci(a, b):
    return (b, a + b)

while True:
    fib1, fib2 = 1, 1

    # Get the latest message id
    print("Getting direct messages")
    dms = api.GetDirectMessages(skip_status=True, full_text=True, return_json=True)
    last_dm = dms["events"][0]
    last_dm_id = last_dm["id"]

    # Request tokens from faucet
    print("Sending 'faucet' to tcrpartyvip")
    dm = api.PostDirectMessage("faucet", screen_name="tcrpartyvip", return_json=True)

    # Wait for message confirmation
    replied = False
    confirmed = False
    retry = False
    while replied == False:
        fib1, fib2 = fibonacci(fib1, fib2)
        print("Sleeping {} minutes".format(fib2))
        time.sleep(fib2 * 60)  # Sleep fibonacci minutes

        dms = api.GetDirectMessages(
            since_id=last_dm_id, skip_status=True, full_text=True, return_json=True
        )
        for dm in dms["events"]:
            if (
                dm["message_create"]["sender_id"]
                == "1029028522843627520"
            ):  
                replied = True
                print("Found reply")
                if dm["message_create"]["message_data"]['text'].find(
                    "You got it."
                ) != -1:
                    confirmed = True
                    print("Done")
                if dm["message_create"]["message_data"]['text'].find(
                    "Ack, I can only let you hit the faucet once per day."
                ) != -1:
                    retry = True
                    print("Need to sleep a bit more")

    if retry == False:
        print("Sleeping one day")
        time.sleep(86400)  # Sleep 1 day
