from fastapi import FastAPI
from pydantic import BaseModel
import requests
import json
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI()

# Allow frontend to communicate with backend (CORS policy)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ollama API URL
OLLAMA_URL = "http://localhost:11434/api/generate"

# Request model
class ChatRequest(BaseModel):
    message: str

history = []  # Chat history

@app.post("/chat")
async def chat(request: ChatRequest):
    history.append(request.message)
    final_prompt = "\n".join(history)

    data = {
        'model': 'gemma2:2b',
        'temperature': 1,
        'prompt': final_prompt,
        'stream': False
    }

    try:
        response = requests.post(OLLAMA_URL, json=data)
        response.raise_for_status()
        result = response.json()
        actual_response = result.get('response', 'Sorry, I couldn’t process that.')

        history.append(actual_response)  # Store response in history
        return {"response": actual_response}
    
    except requests.exceptions.RequestException as e:
        return {"response": f"Error: {str(e)}"}

# Run server with Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
