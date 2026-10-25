
from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Load the trained model
model = joblib.load("superkart_model.joblib")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    # Convert input data to DataFrame
    input_data = pd.DataFrame([data])

    # Generate prediction
    prediction = model.predict(input_data)

    return jsonify({
        "prediction": float(prediction[0])
    })

@app.route("/", methods=["GET"])
def home():
    return "SuperKart Prediction API is running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
