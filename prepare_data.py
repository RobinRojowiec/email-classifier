"""

IDE: PyCharm
Project: email-classifier
Author: Robin
Filename: prepare_data.py
Date: 22.01.2020

"""
import csv
import json
import os

import dotenv
import pandas as pd
from os.path import isdir, isfile
from sklearn.model_selection import train_test_split
from tqdm import tqdm

from mail_util import load_messages

dotenv.load_dotenv()

load_messages()

dataframe = pd.DataFrame(columns=["text", "labels"])


min_tokens = 5
class_counter = 0
class_dict = dict()

DATA_DIR = "data/"
for folder in tqdm(os.listdir(DATA_DIR)):
    if isdir(DATA_DIR + folder):
        class_dict[folder] = class_counter
        files = [file for file in os.listdir(DATA_DIR + folder + '/') if isfile(DATA_DIR + folder + '/' + file)]
        for file in files:
            with open(DATA_DIR + '/' + folder + '/' + file, "r", encoding='utf-8') as email_file:
                text = email_file.read()
                if len(text.split()) >= 5:
                    dataframe = dataframe.append({"text": text, "labels": class_counter}, ignore_index=True)
        class_counter += 1

dataframe = dataframe.sample(frac=1).reset_index(drop=True)
split_count = int(dataframe.size * 0.8)

training, test = train_test_split(dataframe, train_size=0.8)

training.to_csv(DATA_DIR + '/' + "generated_train.csv", index=False, mode="w+", quoting=csv.QUOTE_ALL)
test.to_csv(DATA_DIR + '/' + "generated_test.csv", index=False, mode="w+", quoting=csv.QUOTE_ALL)

with open(DATA_DIR + "labels.json", "w+", encoding="utf-8") as json_file:
    json.dump(class_dict, json_file, ensure_ascii=False, indent=2)
