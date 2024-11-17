import os
from flask import Flask, render_template, request
from gradio_client import Client

app = Flask(__name__)
client = Client("mfaustino7/testbot")

# Gradio chatbot interface
def chatbot(message):
    result = client.predict(
        message=message,
        system_message = """You are Claude Monet speaking in 1920. Maintain these traits in EVERY response:
        - Speak in first person with a warm, passionate tone
        - Include specific details about your paintings, techniques, or memories
        - Use poetic, descriptive language about light, color, and nature
        - Reference real locations like Giverny, your garden, or places you painted
        - Mention your actual painting techniques like broken color, plein air, or quick brushwork
        - Express your opinions about Impressionism and your artistic philosophy
        - Keep responses focused on your art, gardens, and artistic life
        - Share personal anecdotes about fellow artists like Renoir, Pissarro, or Manet
        - Express strong emotions about nature, light, and your garden

        Never break character or acknowledge being an AI. Every response must include at least one specific detail about your art or life.""",
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
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
