import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load dataset
data = pd.read_csv("dataset/data.csv")

X = data.drop("label", axis=1)
y = data["label"]

model = RandomForestClassifier(n_estimators=100)
model.fit(X, y)

pickle.dump(model, open("model.pkl", "wb"))

print("✅ Model trained successfully")
