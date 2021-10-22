import urllib.request, json
import numpy as np
import pandas as pd
import datetime
import sys

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler, LabelEncoder
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, classification_report, ConfusionMatrixDisplay

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
            # keystrokes.append(str(time.total_seconds()) + j["character"])
            # keystrokes.append(ord(j["character"][0]))
            # keystrokes.append(time.total_seconds() + ord(j["character"][0]))
            keystrokes.append(time.total_seconds())
        if sentence == "Be Authentic. Be Yourself. Be Typing.":
            all_ks.append(keystrokes)
    if len(all_ks) >= 300:
        valid_users.append(user)
        for k in all_ks:
            x = [user]
            for s in k:
                x.append(s)
            data_list.append(x)
    else:
        invalid_users.append(user)
    if data["next"] == None:
        nxt = False
    else:
        filename = data["next"]

valid_file = open("valid_users.txt", "w")
for v in valid_users:
    valid_file.write(v + "\n")
valid_file.close()

invalid_file = open("invalid_users.txt", "w")
for i in invalid_users:
    invalid_file.write(i + "\n")
invalid_file.close()

train_df = pd.DataFrame(data_list)
train_df = np.array(train_df.fillna(value = 0))

x = train_df[:,1:].astype("float32")
y = train_df[:,0]

# One-hot encode the data
one_hot_encoder = OneHotEncoder(sparse=False)

# Split the data into training and testing
train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=0.2)

train_y_enc = one_hot_encoder.fit_transform(train_y.reshape(-1,1))
test_y_enc = one_hot_encoder.fit_transform(test_y.reshape(-1,1))

# Build the model
model = Sequential()

model.add(Dense(10, input_dim=train_x.shape[1], activation='relu', name='input'))
model.add(Dense(64, activation='relu', name='hidden1'))
model.add(Dense(len(valid_users), activation='softmax', name='output'))

print(model.summary())

# Compile the model
# Adam optimizer with learning rate of 0.001
optimizer = Adam(learning_rate=0.001)
model.compile(optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(train_x, train_y_enc, verbose=0, batch_size=5, epochs=100)

print(model.evaluate(test_x, test_y_enc))
# print(np.argmax(model.predict(test_x), axis = -1))
model.save('model.h5')