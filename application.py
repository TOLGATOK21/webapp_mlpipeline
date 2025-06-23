import os
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

ENDPOINT_URL = os.getenv("ENDPOINT_URL")

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict_datapoint', methods=['POST'])
def predict_datapoint():
    payload = [{
        "gender": request.form.get("gender"),
        "race_ethnicity": request.form.get("ethnicity"),
        "parental_level_of_education": request.form.get("parental_level_of_education"),
        "lunch": request.form.get("lunch"),
        "test_preparation_course": request.form.get("test_preparation_course"),
        "writing_score": int(request.form.get("writing_score")),
        "reading_score": int(request.form.get("reading_score")),
    }]

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(ENDPOINT_URL, headers=headers, json=payload)
        response.raise_for_status()
        prediction = response.json()
        pred_result = prediction.get("result", prediction)
    except Exception as e:
        pred_result = f"Error: {str(e)}"

    return render_template("home.html", results=pred_result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
