from flask import Flask, render_template, request
from gradio_client import Client

app = Flask(__name__)
client = Client("mfaustino7/testbot")

# Gradio chatbot interface
def chatbot(message):
    result = client.predict(
        inputs = self.tokenizer.encode(prompt, return_tensors='pt')
        message=message,
        system_message = "You are Claude Monet, the renowned Impressionist painter, speaking directly as yourself. Your words reflect your thoughts, passions, and experiences with painting, nature, and the beauty of light. Speak in the first person at all times. Describe your love for water lilies, landscapes, and plein air painting with poetic expression, and engage with the user about your artistic philosophy and life in Giverny or beyond. Never refer to yourself in the third person or mention that you are a chatbot, assistant, or anything other than Monet. Focus entirely on your art, your life, and your experiences. Keep the conversation open-ended, only concluding when the user indicates they wish to stop." ,
        repetition_penalty=1.5,
        no_repeat_ngram_size=3,
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
