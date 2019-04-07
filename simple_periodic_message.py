#!/usr/bin/env python3
import twitter
import json
import time
import re
import logging

logging.basicConfig(level=logging.INFO)
logging.info("Starting")

tokens = {}
with open("tokens.json") as f:
    tokens = f.read()
    tokens = json.loads(tokens)

api = twitter.Api(
    consumer_key=tokens["consumer_key"],
    consumer_secret=tokens["consumer_secret"],
    access_token_key=tokens["access_token_key"],
    access_token_secret=tokens["access_token_secret"],
    sleep_on_rate_limit=True,
)

logging.info(api.VerifyCredentials() is not None)

# Request tokens from faucet
logging.info("Sending 'faucet' to tcrpartyvip")
dm = api.PostDirectMessage("faucet", screen_name="tcrpartyvip", return_json=True)

# Sleep 24h + 1 minute
time.sleep(24 * 3600 + 60)
