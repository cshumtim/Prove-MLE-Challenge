import urllib.request, json
import numpy as np
import pandas as pd
import datetime
import tensorflow as tf

base_url = "https://challenges.unify.id/v1/mle/"
filename = "user_4a438fdede4e11e9b986acde48001122.json"
nxt = True
data_list = []
valid_users = []
invalid_users = []
user_count = 0

while nxt:
    url = base_url + filename
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    user = data["user_label"]
    user_count += 1
    all_ks = []
    for i in range(len(data["user_data"])):
        keystrokes = []
        sentence = ""
        for j in data["user_data"][i]:
            if j["character"] == "[backspace]":
                sentence = sentence[ : -1]
            else:
                sentence = sentence + j["character"]
            time = datetime.datetime.strptime(j["typed_at"], '%Y-%m-%dT%H:%M:%S.%f') - datetime.datetime.strptime(data["user_data"][i][0]["typed_at"], '%Y-%m-%dT%H:%M:%S.%f')
            keystrokes.append((time.total_seconds(), j["character"]))
        if sentence == "Be Authentic. Be Yourself. Be Typing.":
            all_ks.append(keystrokes)
    if len(all_ks) >= 300:
        valid_users.append(user)
        for k in all_ks:
            data_list.append([user, k])
    else:
        invalid_users.append(user)
    if data["next"] == None:
        nxt = False
    else:
        filename = data["next"]

train_df = pd.DataFrame(data_list, columns = ["user_label", "keystroke_data"])

test_list = []
test_url = "https://challenges.unify.id/v1/mle/sample_test.json"
test_response = urllib.request.urlopen(test_url)
test_data = json.loads(test_response.read())

for i in range(len(test_data["attempts"])):
    ks = []
    for d in test_data["attempts"][i]:
        time = datetime.datetime.strptime(d["typed_at"], '%Y-%m-%dT%H:%M:%S.%f') - datetime.datetime.strptime(test_data["attempts"][i][0]["typed_at"], '%Y-%m-%dT%H:%M:%S.%f')
        ks.append((time.total_seconds(), d["character"]))
    test_list.append(ks)

test = [[x] for x in test_list]
test_df = pd.DataFrame(test, columns = ["input_data"])

