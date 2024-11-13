from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize the Flask app and enable CORS
app = Flask(__name__)
CORS(app)

# Configure the Gemini API
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-pro")

# Instructions for Rural Connect-specific responses
context_instructions = (
    "You are an assistant chatbot for the Women Safety platform, designed to empower women & keep them safe. "
    "Keep responses brief, accurate, and specific to context"
)

@app.route('/generate', methods=['POST'])
def generate_response():
    prompt = request.json.get('prompt', '')

    # Generate response from the model based on the user's query
    response = model.generate_content(f"{context_instructions} User: {prompt}")

    # Check if the response contains keywords related to the Rural Connect platform
    if response and any(keyword.lower() in response.text.lower() for keyword in['hi','hello','hii','tourism', 'guide', 'village', 'product', 'course', 'payment', 'escrow', 'transaction']):
        formatted_response = {
            "response": response.text.strip()
        }
    else:
        formatted_response = {
            "response": "I'm here to assist with Women Safety related queries only."
        }

    return jsonify(formatted_response)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
