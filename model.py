import pickle
import numpy as np

# Load trained model
try:
    model = pickle.load(open("model.pkl", "rb"))
except:
    model = None

def predict(features):
    try:
        features = np.array(features).reshape(1, -1)

        if model:
            return model.predict(features)[0]
        else:
            # fallback if model not trained yet
            return "normal"
    except:
        return "normal"