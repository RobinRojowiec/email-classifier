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


def remove_html_tags(text):
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def load_messages():
    # context manager ensures the session is cleaned up
    with IMAPClient(host="outlook.office365.com", port=993) as client:
        client.login(os.getenv('IMAP_USERNAME'), os.getenv('IMAP_PASSWORD'))

        DATA_DIR = "data/"
        folders = client.list_folders()
        for folder in tqdm(folders):
            if folder not in ["Inbox", "Junk", "Drafts", "Deleted"]:

                folder_path = DATA_DIR + folder[-1]
                if os.path.exists(folder_path):
                    shutil.rmtree(folder_path, ignore_errors=False, onerror=None)
                os.mkdir(folder_path)

                client.select_folder(folder[-1])

                # search criteria are passed in a straightforward way
                # (nesting is supported)
                messages = client.search(["NOT", "UNSEEN"])
                messages = messages[:50]

                # `response` is keyed by message id and contains parsed,
                # converted response items.
                for uid, message_data in client.fetch(messages, ['RFC822']).items():
                    email_message = email.message_from_bytes(message_data[b'RFC822'])
                    print(uid, email_message.get('From'), email_message.get('Subject'))

                    with open(folder_path + '/' + str(uid) + ".txt", "w+", encoding="utf-8") as email_file:
                        content = email_message.get('Subject')
                        if content is not None:
                            email_file.write(content)


if __name__ == '__main__':
    import dotenv

    dotenv.load_dotenv()

    load_messages()
