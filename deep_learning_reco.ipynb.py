import os, sys
sys.path.append("..")

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import src.models.deep_reco

df = pd.read_csv("../data/healthcare_dataset.csv")

user_enc = LabelEncoder()
item_enc = LabelEncoder()

users = user_enc.fit_transform(df["Name"].astype(str))
items = item_enc.fit_transform(df["Medication"].astype(str))
labels = (df["Test Results"].astype(str) == "Normal").astype(int).values

n = 2000 if len(users) > 2000 else len(users)
users_s, items_s, labels_s = users[:n], items[:n], labels[:n]

model = DeepRecommender(len(user_enc.classes_), len(item_enc.classes_))
model.train(users_s, items_s, labels_s, epochs=1, batch_size=256)

print("Sample prediction:", model.predict(users_s[0], items_s[0]))
