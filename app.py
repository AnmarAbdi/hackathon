from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

# Global variable to store the conversation context
conversation_history = []

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/chatbox")
def chatbox():
    return render_template('chatbox.html')

@app.route("/resources")
def resources():
    return render_template('medresources.html')

@app.route("/patient")
def patient():
    return render_template('patient.html')

@app.route("/professional")
def professional():
    return render_template('professional.html')

@app.route("/simulator")
def simulator():
    return render_template('simulatorchat.html')

@app.route("/consultation", methods=["POST"])
def consultation():
    global conversation_history

    data = request.get_json()
    user_message = data.get("message")

    if user_message is None:
        return "Invalid message", 400

    # Add each user message to conversation history so the bot doesnt forget
    conversation_history.append({"role": "user", "content": user_message})

    # Process user message
    response_message = process_user_message(user_message)

    # Add bot response to conversation history
    conversation_history.append({"role": "system", "content": response_message})
    
    return jsonify({"response": response_message})

def process_user_message(message):
    global conversation_history

    ai_directive = ("The following conversation is with an AI assistant designed to help users understand "
                    "what to discuss with their doctor about their health concerns. "
                    "The assistant does not provide medical advice but helps in framing the user's symptoms for a medical consultation.")

    # Add the directive to the beginning of the conversation for this request
    messages_with_directive = [{"role": "system", "content": ai_directive}] + conversation_history

    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            json={
                "model": "gpt-4",
                "messages": messages_with_directive
            },
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}"
            }
        )

        if response.status_code != 200:
            return f"Error: Received status code {response.status_code}, details: {response.text}"

        response_data = response.json()
        if 'choices' not in response_data or not response_data['choices'] or not response_data['choices'][0]['message']['content']:
            return "Error: 'choices' not found in the response or empty"

        return response_data['choices'][0]['message']['content'].strip()

    except Exception as e:
        return f"An unexpected error occurred: {e}"

''' 
Tried implementing a way to clear the conversation_history but i couldnt figure it out

@app.route("/clear-conversation", methods=["POST"])
def clear_conversation():
    global conversation_history
    conversation_history = []
    return "", 200  # Return an empty response with a 200 OK status

@app.route("/debug/conversation_history")
def debug_conversation_history():
    global conversation_history
    return jsonify(conversation_history)
'''

if __name__ == "__main__":
    app.run(debug=True)
