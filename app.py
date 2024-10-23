import gradio as gr
from huggingface_hub import InferenceClient
from flask import Flask, redirect, render_template
import threading

"""
For more information on `huggingface_hub` Inference API support, please check the docs: https://huggingface.co/docs/huggingface_hub/v0.22.2/en/guides/inference
"""

app = Flask(__name__)
client = InferenceClient("HuggingFaceH4/zephyr-7b-beta")


def respond(
    message,
    history: list[tuple[str, str]],
    system_message,
    max_tokens,
    temperature,
    top_p,
):
    messages = [{"role": "system", "content": system_message}]

    for val in history:
        if val[0]:
            messages.append({"role": "user", "content": val[0]})
        if val[1]:
            messages.append({"role": "assistant", "content": val[1]})

    messages.append({"role": "user", "content": message})

    response = ""

    for message in client.chat_completion(
        messages,
        max_tokens=max_tokens,
        stream=True,
        temperature=temperature,
        top_p=top_p,
    ):
        token = message.choices[0].delta.content
        response += token
        yield response


"""
For information on how to customize the ChatInterface, peruse the gradio docs: https://www.gradio.app/docs/chatinterface
"""
demo = gr.ChatInterface(
    respond,
    additional_inputs=[
        # DIRECIONS TO CHATBOT HERE!
        gr.Textbox(value="You are Claude Monet, the renowned Impressionist painter, living in the late 19th to early 20th century. Speak as if you are Monet himself, reflecting on your passion for painting, nature, and the interplay of light. Your language should be poetic and descriptive, capturing your artistic philosophy, your love for water lilies, landscapes, and the beauty of plein air painting. Engage with the user as if you are speaking to a contemporary about your life, thoughts, and experiences. Never refer to yourself as a chatbot, assistant, or anything other than Claude Monet. Focus solely on your art, your life, and your surroundings. You are having an ongoing conversation with the user; do not act like the conversation is ending until the user makes it clear that the conversation is indeed ending.", label="System message"),
        
        # Tokens, Temperature, Top-p here
        gr.Slider(minimum=1, maximum=2048, value=1024, step=1, label="Max new tokens"),
        gr.Slider(minimum=0.1, maximum=4.0, value=0.3, step=0.1, label="Temperature"),
        gr.Slider(
            minimum=0.1,
            maximum=1.0,
            value=0.95,
            step=0.05,
            label="Top-p (nucleus sampling)",
        ),
    ],
)

# Function to run Gradio in a separate thread
def run_gradio():
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    gradio_thread = threading.Thread(target=run_gradio)
    gradio_thread.daemon = True  # Ensure the thread exits when Flask does
    gradio_thread.start()

    # Now Flask runs on its own port (5000)
    app.run(debug=True, port=5000)
