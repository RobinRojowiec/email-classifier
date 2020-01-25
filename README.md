# email-classifier
Tool to classify emails in outlook and move them into corresponding folders

## Installation

The scripts have bin tested in Python 3.6.5. 

Install the required dependencies using pip:
``bash
pip3 install -r requirements.txt
``

Then, create a `.env` file and store your credentials for outlook (your login username and password):

``bash
IMAP_USERNAME=username
IMAP_PASSWORD=password
``

Following, the `prepare_data.py` script downloads all first level folders and a maximum of 50 mails from each
folder (excluding spam, inbox, etc.). The classifier script trains a german transformer model to identify which
folder the mail belongs to and saves it.

To clean your inbox, run `python3 put_emails_in_folders.py`. This script requires your mail provider to support the MOVE capability.
