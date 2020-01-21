"""

IDE: PyCharm
Project: email-classifier
Author: Robin
Filename: mail_util.py
Date: 20.01.2020

"""
import email
import os

from imapclient import IMAPClient


def load_messages():
    # context manager ensures the session is cleaned up
    with IMAPClient(host="outlook.office365.com", port=993) as client:
        client.login(os.getenv('IMAP_USERNAME'), os.getenv('IMAP_PASSWORD'))

        print(client.folder_exists('INBOX'))
        client.select_folder('INBOX')

        # search criteria are passed in a straightforward way
        # (nesting is supported)
        messages = client.search(['FLAGGED'])
        print(len(messages))

        # `response` is keyed by message id and contains parsed,
        # converted response items.
        for uid, message_data in client.fetch(messages, ['RFC822', 'BODY']).items():
            email_message = email.message_from_bytes(message_data[b'RFC822'])
            print(uid, email_message.get('From'), email_message.get('Subject'))


if __name__ == '__main__':
    import dotenv

    dotenv.load_dotenv()

    load_messages()
