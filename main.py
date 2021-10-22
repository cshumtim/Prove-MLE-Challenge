import urllib.request, json
import numpy as np
import pandas as pd
import datetime
import sys

import tensorflow as tf
from tensorflow import keras

with open("valid_users.txt") as file:
    lines = file.readlines()
    labels = [line.rstrip() for line in lines]

model = keras.models.load_model('model.h5')

data_list = []
url = sys.argv[1]
response = urllib.request.urlopen(url)
data = json.loads(response.read())

for i in range(len(data["attempts"])):
    ks = []
    sentence = ""
    for d in data["attempts"][i]:
        if d["character"] == "[backspace]":
            sentence = sentence[ : -1]
        else:
            sentence = sentence + d["character"]
        time = datetime.datetime.strptime(d["typed_at"], '%Y-%m-%dT%H:%M:%S.%f') - datetime.datetime.strptime(data["attempts"][i][0]["typed_at"], '%Y-%m-%dT%H:%M:%S.%f')
        ks.append(time.total_seconds())
    if sentence == "Be Authentic. Be Yourself. Be Typing.":
        data_list.append(ks)
    else:
        data_list.append(["Invalid"])

output = []
for e in data_list:
    if e[0] == "Invalid":
        output.append("Invalid Input")
    else:
        if len(e) != 41:
            for i in range(41 - len(e)):
                e.append(0)
        e = [e]
        df = np.array(e).astype("float32")
        user_class = np.argmax(model.predict(df), axis = -1)
        output.append(labels[user_class[0]])
print(output)