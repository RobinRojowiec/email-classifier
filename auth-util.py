"""

IDE: PyCharm
Project: email-classifier
Author: Robin
Filename: auth-util.py
Date: 19.01.2020

"""
import os

import requests
from dotenv import load_dotenv

load_dotenv()


def get_access_token():
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    body = {
        'grant_type': 'client_credentials',
        'client_id': os.getenv("CLIENT_ID"),
        'scope': 'https://graph.microsoft.com/.default',
        'client_secret': os.getenv("CLIENT_SECRET")
    }

    response = requests.post(os.getenv("AUTH_URL"), headers=headers, data=body)
    if response.status_code == 200:
        return response.json()["access_token"]
    return None


token = get_access_token()
print(token)
