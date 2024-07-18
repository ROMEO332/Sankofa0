import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
import json

# Set the environment variable for protobuf
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

app = Flask(__name__)
CORS(app)  # Enable CORS

# Load the Twi language model and tokenizer
model_name = "Ghana-NLP/distilabena-base-akuapem-twi-cased"
model = AutoModelForSequenceClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
nlp_pipeline = pipeline("text-classification", model=model, tokenizer=tokenizer)

# Dr. Laurence's details
dr_laurence_details = {
    "name": "Dr. Laurence",
    "phone": "+233 24 123 4567",
    "email": "dr.laurence@example.com",
    "address": "123 Health St, Accra, Ghana"
}

# Load health advice data from JSON file
with open('health_data.json', 'r', encoding='utf-8') as f:
    health_data = json.load(f)

def get_health_advice(query):
    for entry in health_data:
        if entry["symptom"] in query:
            return entry["advice"]
    return "Mepa wo kyɛw, nsɛm a mede ma wo yɛ nhyehyɛe. Kɔhwɛ dɔkotani sɛ ɛyɛ den."

def refer_to_dr_laurence():
    return (f"Yɛfrɛ Dr. Laurence wɔ {dr_laurence_details['phone']} anaa bɔ no email wɔ "
            f"{dr_laurence_details['email']}.")

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    user_query = data.get('query').lower()

    # Get health advice based on the query
    advice = get_health_advice(user_query)

    # Check for keywords to refer to Dr. Laurence
    if "emergency" in user_query or "serious" in user_query:
        advice += "\n\n" + refer_to_dr_laurence()

    return jsonify({"response": advice})

if __name__ == '__main__':
    app.run(debug=True)
