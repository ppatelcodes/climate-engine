import os
from dotenv import load_dotenv
from kiteconnect import KiteConnect

load_dotenv()

api_key = os.getenv("KITE_API_KEY")
api_secret = os.getenv("KITE_API_SECRET")

kite = KiteConnect(api_key = api_key)

#step 1: open this URL in your browser and login
print("Login URL:")
print(kite.login_url())

# step 2: after login, copy the request_token from the redirected URL
request_token = input("Paste request_token here: ").strip()

# step 3: generate access token
data = kite.generate_session(request_token, api_secret = api_secret)
access_token = data["access_token"]

print("\nYour access token:")
print(access_token)
print("\nPaste this into your .env file as KITE_ACCESS_TOKEN")