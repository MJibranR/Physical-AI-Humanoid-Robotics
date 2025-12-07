from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import google.generativeai as genai

app = FastAPI()

# Enhanced CORS settings - allow your frontend domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # for local development
        "https://physical-ai-humanoid-robotics-three.vercel.app/",
        "https://www.physical-ai-humanoid-robotics-three.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Configure Gemini API key - with fallback
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyBoS-XQy7UhJc8tYXQ-TrpOf_FWP_wg6gs")
genai.configure(api_key=GEMINI_API_KEY)

class ChatRequest(BaseModel):
    message: str

@app.get("/")
async def root():
    return {"message": "Physical AI Humanoid Robotics Backend is live!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Physical AI Humanoid Robotics"}
@app.post("/api/chat")
async def chat(req: ChatRequest):
    try:
        if not req.message or req.message.strip() == "":
            return {"response": "Message cannot be empty"}
        
        model = genai.GenerativeModel("models/gemini-2.0-flash")

        system_prompt = """"""

        full_prompt = f"{system_prompt}\n\nUser: {req.message}\nAssistant:"
        
        response = model.generate_content(full_prompt)
        return {"response": response.text}

    except Exception as e:
        return {"response": f"Error: {str(e)}"}

@app.options("/api/chat")
async def options_chat():
    return {"message": "OK"}