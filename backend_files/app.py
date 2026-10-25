
from flask import Flask, request, jsonify
import joblib
import pandas as pd

superkart_api = Flask(__name__)

# Load the trained model
model = joblib.load("superkart_model.joblib")

# Columns expected by the trained model
model_columns = list(model.feature_names_in_)


def preprocess(data):
    # Convert input to DataFrame
    input_data = pd.DataFrame(data)

    # Fix inconsistent sugar-content label
    input_data['Product_Sugar_Content'] = (
        input_data['Product_Sugar_Content'].replace('reg', 'Regular')
    )

    # Product_Id was excluded during model training
    if 'Product_Id' in input_data.columns:
        input_data.drop('Product_Id', axis=1, inplace=True)

    # One-hot encode categorical variables
    input_data = pd.get_dummies(input_data, drop_first=True)

    # Match the exact columns used during model training
    input_data = input_data.reindex(columns=model_columns, fill_value=0)

    return input_data


@superkart_api.post("/v1/predict")
def predict():
    data = request.get_json()

    input_data = preprocess([data])
    prediction = model.predict(input_data)

    return jsonify({
        "prediction": float(prediction[0])
    })


@superkart_api.post("/v1/predictbatch")
def predict_batch():
    data = request.get_json()

    input_data = preprocess(data)
    predictions = model.predict(input_data)

    return jsonify({
        "predictions": predictions.tolist()
    })


if __name__ == "__main__":
    superkart_api.run(host="0.0.0.0", port=7860)
