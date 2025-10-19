from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os
import uvicorn

app = FastAPI()


GEMINI_API_KEY = ""
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

class StoryRequest(BaseModel):
    prompt: str
    max_tokens: int = 3000

@app.post("/generate-story")
def generate_story(request: StoryRequest):
    headers = {
        "Content-Type": "application/json"
    }
    params = {
        "key": GEMINI_API_KEY
    }
    payload = {
        "contents": [
            {"parts": [{"text": f"Write a creative story based on: {request.prompt}"}]}
        ],
        "generationConfig": {
            "maxOutputTokens": request.max_tokens
        }
    }

    response = requests.post(GEMINI_API_URL, headers=headers, params=params, json=payload)


    

    if response.status_code != 200:
        return {"error": response.text}

    data = response.json()
    story_text = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")

    return {"story": story_text}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
