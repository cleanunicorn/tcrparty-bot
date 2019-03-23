import twitter
import json
import time

with open("tokens.json") as f:
    tokens = f.read()
    tokens = json.load(tokens)

api = twitter.Api(
    consumer_key=tokens["consumer_key"],
    consumer_secret=tokens["consumer_secret"],
    access_token_key=tokens["access_token"],
    access_token_secret=tokens["access_token_secret"],
)

print(api.VerifyCredentials())
# {"id": 16133, "location": "Philadelphia", "name": "bear"}

# Start
# Send message
# Wait for confirmation
# End

while True:
    fib1, fib2 = 1, 1

    # Get the latest message id
    dms = api.GetDirectMessages(skip_status=True, full_text=True, return_json=True)
    last_dm = dms[len(dms) - 1]
    last_dm_id = last_dm["message_id"]  # TODO: Replace with correct key

    # Request tokens from faucet
    dm = api.PostDirectMessage("faucet", user_id="tcrparty", return_json=True)
    print(dm)

    # Wait for message confirmation
    replied = False
    confirmed = False
    retry = False
    while replied == False:
        fib1, fib2 = fibonacci(fib1, fib2)
        time.sleep(fib2 * 60)  # Sleep fibonacci minutes

        dms = api.GetDirectMessages(
            since_id=last_dm_id, skip_status=True, full_text=True, return_json=True
        )
        dms = json.load(dms)
        for dm in dms:
            if dm["user_id"] == "tcrparty":  # TODO: Replace with user_id
                replied = True
                if dm["message"].find(
                    "Your message is confirmed"
                ):  # TODO: Replace with key and text
                    confirmed = True
                if dm["message"].find(
                    "Too early to send message"
                ):  # TODO: Replace with key and text
                    retry = True

    if retry == False:
        time.sleep(86400)  # Sleep 1 day


def fibonacci(a, b):
    return (b, a + b)

