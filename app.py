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
    background: #4F6D7A;  /* Muted blue-grey */
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
    background-color: #F5E6CA;  /* Light aged paper color */
    color: #2C4A52;  /* Dark blue-grey for text */
    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
}

.gradio-container .gr-textbox:focus {
    border-color: #6B4423;  /* Darker sepia on focus */
    outline: none;
}

.gradio-container {
    background: #F3E5AB;  /* Vintage paper yellow */
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
    background-image: url('data:image/png;base64,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');
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
