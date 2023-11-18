from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

@app.route("/consultation", methods=["POST"])
def consultation():
    data = request.get_json()
    user_message = data.get("message")

    if user_message is None:
        return "Invalid message", 400
    # Process user message
    response_message = process_user_message(user_message)
    
    return jsonify({"response": response_message})

def process_user_message(message):
    # Processes message and generates response
    response = requests.post(
        "https://api.openai.com/v1/completions",
        json={
            "model": "gpt-4",
            "prompt": generate_prompt(message),
            "max_tokens": 150,
            "temperature": 0.7,
        },
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }
    )

    if response.status_code == 200 and 'choices' in response.json() and response.json()['choices']:
        return response.json()['choices'][0]['text'].strip()
    else:
        return "I'm sorry, I couldn't process your request."

def generate_prompt(user_input):
    # customize how we want to prompt the model based on user input
    return f"User: {user_input}\nAI:"

if __name__ == "__main__":
    app.run(debug=True)
