"""

IDE: PyCharm
Project: email-classifier
Author: Robin
Filename: auth_util.py
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
        'scope': os.getenv("SCOPES"),
        'client_secret': os.getenv("CLIENT_SECRET")
    }

    response = requests.post(os.getenv("AUTH_URL"), headers=headers, data=body)
    if response.status_code == 200:
        token = response.json()["access_token"]
        return token, {'Authorization': 'Bearer ' + token, 'outlook.body-content-type': 'html'}
    return None

