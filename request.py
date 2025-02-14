# using ollama API to use the model in the therapist application.

import requests
import json
import gradio as gr

url="http://localhost:11434/api/generate"

headers={
    'content-type': 'application/json' ,
}

history=[]

def generate_response(prompt):
    history.append(prompt)
    final_prompt="\n".join(history)

    data={
        'model': 'gemma2:2b',
        'temperature': 1,
        'prompt': final_prompt,
        'stream': False
    }

    response=requests.post(url,headers=headers,data=json.dumps(data))

    if response.status_code==200:
         response=response.text
         data=json.loads(response)
         actual_response=data['response']
         return actual_response
    else:
         return "Error: Unable to generate response."
    
interface=gr.Interface(
     fn=generate_response,
     inputs=gr.Textbox(label="Type anything on your mind. No judgment, just support."),
     outputs=gr.Textbox(label="Hello! I'm here to listen. How are you feeling today? ")
)
