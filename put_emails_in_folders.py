"""

IDE: PyCharm
Project: email-classifier
Author: Robin
Filename: put_emails_in_folders.py
Date: 23.01.2020

"""

import json
# load the model
import os

import dotenv
import torch
from imapclient import IMAPClient
from simpletransformers.classification import ClassificationModel
from torch.nn.functional import softmax

from mail_util import load_inbox_folder

dotenv.load_dotenv()
model = ClassificationModel("bert", "outputs/", num_labels=30, args={'use_multiprocessing': False, 'fp16': False})

inbox_messages = load_inbox_folder()

labels = dict()
with open("data/labels.json", "r", encoding="utf-8") as label_file:
    raw_labels = json.loads(label_file.read())
    for key in raw_labels.keys():
        labels[raw_labels[key]] = key

with IMAPClient(host="outlook.office365.com", port=993) as client:
    client.login(os.getenv('IMAP_USERNAME'), os.getenv('IMAP_PASSWORD'))
    client.select_folder("Inbox")

    for mail_tuple in inbox_messages:
        text = mail_tuple[1].get('Subject')

        predictions, raw_outputs = model.predict([text])
        probabilities = softmax(torch.from_numpy(raw_outputs).float(), dim=1)
        label = labels[predictions[0]]
        prob = probabilities[0][predictions[0]].item()

        if prob >= 0.2:
            print(text, prob, label)
            client.add_flags([mail_tuple[0]], "CLASSIFIED")
            print(client.move([mail_tuple[0]], label))
