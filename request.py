import requests
import json
import gradio as gr

# Ollama API URL
url = "http://localhost:11434/api/generate"

headers = {
    'Content-Type': 'application/json',
}

history = []  # Store chat history

def generate_response(prompt):
    history.append(prompt)  # Store user input
    final_prompt = "\n".join(history)  # Maintain conversation history

    # Request payload
    data = {
        'model': 'gemma2:2b',  # Ensure you have this model downloaded in Ollama
        'temperature': 1,
        'prompt': final_prompt,
        'stream': False  # Change to True if you want streaming responses
    }

    # Send request to Ollama API
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
        
        result = response.json()
        actual_response = result.get('response', 'Sorry, I couldn’t process that.')
        
        history.append(actual_response)  # Store AI's response
        return actual_response

    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"

# Gradio Interface
interface = gr.Interface(
    fn=generate_response,
    inputs=gr.Textbox(label="Type anything on your mind. No judgment, just support."),
    outputs=gr.Textbox(label="Hello! I'm here to listen. How are you feeling today?"),
    live=True  # Ensure the interface updates in real-time
)

# Launch Gradio App
interface.launch()
