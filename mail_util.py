"""

IDE: PyCharm
Project: email-classifier
Author: Robin
Filename: mail_util.py
Date: 20.01.2020

"""
import email
import os
import re
import shutil

from imapclient import IMAPClient
from tqdm import tqdm

DATA_DIR = "data/"
default_folder_list = ["Inbox", "Junk", "Drafts", "Deleted", "Outbox", "Sent", "Archive"]


def remove_html_tags(text):
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def load_inbox_folder():
    mail_list = []

    # context manager ensures the session is cleaned up
    with IMAPClient(host="outlook.office365.com", port=993) as client:
        client.login(os.getenv('IMAP_USERNAME'), os.getenv('IMAP_PASSWORD'))

        # select inbox
        client.select_folder('Inbox')

        # search criteria are passed in a straightforward way
        # (nesting is supported)
        messages = client.search(["SEEN"])
        messages = messages[:200]

        # `response` is keyed by message id and contains parsed,
        # converted response items.
        for uid, message_data in client.fetch(messages, ['RFC822']).items():
            email_message = email.message_from_bytes(message_data[b'RFC822'])
            mail_list.append((uid, email_message))
    return mail_list


def load_messages():
    shutil.rmtree(DATA_DIR, ignore_errors=False, onerror=None)
    os.mkdir(DATA_DIR)

    # context manager ensures the session is cleaned up
    with IMAPClient(host="outlook.office365.com", port=993) as client:
        client.login(os.getenv('IMAP_USERNAME'), os.getenv('IMAP_PASSWORD'))

        folders = [folder[-1] for folder in client.list_folders() if
                   folder[-1] not in default_folder_list and not "/" in folder[-1]]
        for folder in tqdm(folders):
            folder_path = DATA_DIR + folder
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path, ignore_errors=False, onerror=None)
            os.mkdir(folder_path)

            client.select_folder(folder)

            # search criteria are passed in a straightforward way
            # (nesting is supported)
            messages = client.search(["SEEN"])
            messages = messages[:50]

            # `response` is keyed by message id and contains parsed,
            # converted response items.
            for uid, message_data in client.fetch(messages, ['RFC822']).items():
                email_message = email.message_from_bytes(message_data[b'RFC822'])
                content = email_message.get('Subject')
                print(uid, email_message.get('From'), content)

                with open(folder_path + '/' + str(uid) + ".txt", "w+", encoding="utf-8") as email_file:
                    if content is not None:
                        email_file.write(content)


if __name__ == '__main__':
    import dotenv

    dotenv.load_dotenv()

    load_messages()
