import urllib.request, json
import numpy as np
import pandas as pd
import datetime

import tensorflow as tf
from tensorflow import keras

import matplotlib.pyplot as plt

labels = ["4a438fdede4e11e9b986acde48001122",
        "4a45245cde4e11e9b51bacde48001122",
        "4a4558dcde4e11e9bbfaacde48001122",
        "4a45bafade4e11e99e37acde48001122",
        "4a45f03ade4e11e9922cacde48001122",
        "4a4626c2de4e11e98c17acde48001122",
        "4a466e5cde4e11e98e06acde48001122",
        "4a46a7a8de4e11e99efeacde48001122",
        "4a46debede4e11e996d6acde48001122",
        "4a47153ade4e11e9a04eacde48001122",
        "4a474bf6de4e11e980dbacde48001122",
        "4a47885ade4e11e98c41acde48001122",
        "4a482be8de4e11e9a2a2acde48001122",
        "4a486266de4e11e98893acde48001122",
        "4a4898e4de4e11e98573acde48001122",
        "4a4905d8de4e11e99a50acde48001122",
        "4a493c4ade4e11e99e33acde48001122",
        "4a497764de4e11e9bc80acde48001122",
        "4a49ae0ade4e11e9b2d3acde48001122",
        "4a49e492de4e11e98206acde48001122",
        "4a4a1b1ade4e11e9a868acde48001122",
        "4a4a518cde4e11e99ae3acde48001122",
        "4a4a8802de4e11e9a447acde48001122",
        "4a4abe80de4e11e9963bacde48001122",
        "4a4af4fede4e11e9b4c8acde48001122",
        "4a4b2b86de4e11e99e25acde48001122",
        "4a4b6358de4e11e9b361acde48001122",
        "4a4b99d8de4e11e9ab53acde48001122",
        "4a4bd05ede4e11e987bfacde48001122",
        "4a4c06f0de4e11e997dfacde48001122",
        "4a4c3d6ede4e11e98e3bacde48001122",
        "4a4c73e2de4e11e98b63acde48001122",
        "4a4ce17ede4e11e9a181acde48001122",
        "4a4d17f4de4e11e9bdbaacde48001122",
        "4a4d4e70de4e11e9a835acde48001122",
]

model = keras.models.load_model('model.h5')

test_list = []
test_url = "https://challenges.unify.id/v1/mle/sample_test.json"
test_response = urllib.request.urlopen(test_url)
test_data = json.loads(test_response.read())

for i in range(len(test_data["attempts"])):
    ks = []
    test_sentence = ""
    for d in test_data["attempts"][i]:
        if d["character"] == "[backspace]":
            test_sentence = test_sentence[ : -1]
        else:
            test_sentence = test_sentence + d["character"]
        time = datetime.datetime.strptime(d["typed_at"], '%Y-%m-%dT%H:%M:%S.%f') - datetime.datetime.strptime(test_data["attempts"][i][0]["typed_at"], '%Y-%m-%dT%H:%M:%S.%f')
        ks.append(time.total_seconds())
    if test_sentence == "Be Authentic. Be Yourself. Be Typing.":
        test_list.append(ks)
    else:
        test_list.append(["Invalid"])

output = []
count = {}
for i in range(len(labels)):
    count[str(i)] = 0
for e in test_list:
    if e[0] == "Invalid":
        output.append("Invalid Input")
        if "Invalid" not in count:
            count["Invalid"] = 1
        else:
            count["Invalid"] = count["Invalid"] + 1
    else:
        if len(e) != 41:
            for i in range(41 - len(e)):
                e.append(0)
        e = [e]
        test_df = np.array(e).astype("float32")
        user_class = np.argmax(model.predict(test_df), axis = -1)
        count[str(user_class[0])] = count[str(user_class[0])] + 1
        output.append(labels[user_class[0]])

# print(output)

plt.bar(range(len(count)), list(count.values()), align='center')
plt.xticks(range(len(count)), list(count.keys()))

plt.show()

plt2.bar(range(2), [35, 5], align='center')
plt2.xticks(range(2), ["Valid", "Invalid"])

plt2.show()