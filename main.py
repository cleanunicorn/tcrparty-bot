import twitter
import json

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

dm = api.PostDirectMessage("faucet", user_id="tcrparty")
print(dm.AsDict())

while True:
    dms = api.GetDirectMessages(skip_status=True, full_text=True, return_json=True)
    dms = json.load(dms)
    for dm in dms:
        # dm = dm.AsDict()
        # dm['']
        print(dm)
