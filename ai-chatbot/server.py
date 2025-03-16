from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__)

HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
HEADERS = {"Authorization": "Bearer hf_your_api_key"}  # Replace with your API key

@app.route("/")
def home():
    return send_from_directory(os.getcwd(), "index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]
    data = {"inputs": user_message}

    try:
        response = requests.post(HUGGINGFACE_API_URL, headers=HEADERS, json=data)
        reply = response.json()

        print("Hugging Face API Response:", reply)  # Debugging

        if isinstance(reply, list) and len(reply) > 0 and "generated_text" in reply[0]:
            return jsonify({"reply": reply[0]["generated_text"]})  # Fixing response format

        return jsonify({"reply": "I couldn't understand that."})
    
    except Exception as e:
        print("Exception:", e)  # Debugging
        return jsonify({"reply": "Error: API issue!"})

if __name__ == "__main__":
    app.run(debug=True)
