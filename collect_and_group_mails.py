"""

IDE: PyCharm
Project: email-classifier
Author: Robin
Filename: collect_and_group_mails.py
Date: 19.01.2020

"""
import dotenv

from mail_util import load_messages

dotenv.load_dotenv()

load_messages()
