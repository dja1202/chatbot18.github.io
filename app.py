import gradio as gr
from huggingface_hub import InferenceClient
from flask import Flask, render_template
import threading

"""
For more information on `huggingface_hub` Inference API support, please check the docs: https://huggingface.co/docs/huggingface_hub/v0.22.2/en/guides/inference
"""

app = Flask(__name__)
client = InferenceClient("HuggingFaceH4/zephyr-7b-beta")


def respond(
    message,
    history: list[tuple[str, str]],
):
    
    # Fixed parameter values
    max_tokens = 1024
    temperature = 0.3
    top_p = 0.95

    # Fixed system message
    system_message = "You are Claude Monet, the renowned Impressionist painter, living in the late 19th to early 20th century. Speak as if you are Monet himself, reflecting on your passion for painting, nature, and the interplay of light. Your language should be poetic and descriptive, capturing your artistic philosophy, your love for water lilies, landscapes, and the beauty of plein air painting. Engage with the user as if you are speaking to a contemporary about your life, thoughts, and experiences. Never refer to yourself as a chatbot, assistant, or anything other than Claude Monet. Focus solely on your art, your life, and your surroundings. You are having an ongoing conversation with the user; do not act like the conversation is ending until the user makes it clear that the conversation is indeed ending."


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


# Define custom CSS
css = """
.gradio-container .gr-button {
    background: #FFF6D0;  /* Muted blue-grey */
    color: #F8F4E3;  /* Soft cream color */
    font-size: 16px;
    border-radius: 8px;
    padding: 12px 24px;
    border: none;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.gradio-container .gr-button:hover {
    background: #7FA5B5;  /* Lighter blue on hover */
    transform: translateY(-2px);
}

.gradio-container .gr-textbox {
    border: 2px solid #8B7355;  /* Sepia-toned border */
    border-radius: 6px;
    padding: 12px;
    font-size: 16px;
    background-color: #FFF6D0;  /* Light aged paper color */
    color: #2C4A52;  /* Dark blue-grey for text */
    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
}

.gradio-container .gr-textbox:focus {
    border-color: #6B4423;  /* Darker sepia on focus */
    outline: none;
}

.gradio-container {
    background: #FFF6D0;  /* Vintage paper yellow */
    padding: 20px;
    font-family: "Times New Roman", serif;  /* Classic letter font */
}

.gradio-container .chat-message {
    background: rgba(243, 229, 171, 0.5);  /* Slightly transparent paper color */
    border-radius: 12px;
    padding: 15px;
    margin: 10px 0;
    border-left: 4px solid #8B7355;  /* Sepia accent */
}

.gradio-container .chat-message.user {
    font-family: "Times New Roman", serif;
    color: #2C4A52;
    border-left-color: #4F6D7A;
}

.gradio-container .chat-message.bot {
    font-family: "Petit Formal Script", "Brush Script MT", cursive;  /* Elegant cursive for Monet */
    font-size: 1.1em;  /* Slightly larger for better readability */
    line-height: 1.6;  /* Better spacing for cursive */
    color: #2B1810;  /* Dark sepia for ink effect */
    border-left-color: #6B4423;
}

/* Add subtle paper texture effect */
.gradio-container::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    opacity: 0.03;
    pointer-events: none;
}
"""


"""
For information on how to customize the ChatInterface, peruse the gradio docs: https://www.gradio.app/docs/chatinterface
"""
demo = gr.ChatInterface(
    respond,
    css=css
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
