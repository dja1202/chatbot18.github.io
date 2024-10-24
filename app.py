from flask import Flask, render_template, request
from gradio_client import Client

app = Flask(__name__)
client = Client("mfaustino7/testbot")

# Define your Gradio chatbot interface
def chatbot(message):
    result = client.predict(
        message=message,
        system_message="You are a friendly Chatbot.",
        max_tokens=512,
        temperature=0.7,
        top_p=0.95,
        api_name="/chat"
    )
    return result

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/chatbot", methods=["POST"])
def chat():
    input_text = request.json['message']
    response = chatbot(input_text)
    return {"response": response}

if __name__ == "__main__":
    app.run()
