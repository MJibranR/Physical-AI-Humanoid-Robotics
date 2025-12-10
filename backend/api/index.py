from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
import os

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Backend running on Vercel!"}

# Your existing FastAPI endpoints go here
# Your AI, embeddings, Qdrant, Gemini code stays the same

handler = app  # Important for Vercel Python runtime
