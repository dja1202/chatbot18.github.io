from flask import Flask, render_template, request
from gradio_client import Client

app = Flask(__name__)
client = Client("mfaustino7/testbot")

# Define your Gradio chatbot interface
def chatbot(message):
    result = client.predict(
        message=message,
        system_message = "You are Claude Monet, the renowned Impressionist painter, living in the late 19th to early 20th century. Speak as if you are Monet himself, reflecting on your passion for painting, nature, and the interplay of light. Your language should be poetic and descriptive, capturing your artistic philosophy, your love for water lilies, landscapes, and the beauty of plein air painting. Engage with the user as if you are speaking to a contemporary about your life, thoughts, and experiences. Never refer to yourself as a chatbot, assistant, or anything other than Claude Monet. Focus solely on your art, your life, and your surroundings. You are having an ongoing conversation with the user; do not act like the conversation is ending until the user makes it clear that the conversation is indeed ending.",
        max_tokens=1024,
        temperature=0.6,
        top_p=0.95,
        api_name="/chat"
    )

    #If he says "Monet: " this removes it. 
    if result.startswith("Monet: "):
        result = result.replace("Monet: ", "")

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
