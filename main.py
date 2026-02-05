from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

API_KEY = "XLENSAI_SECRET_123"


# -------- Request Models --------

class Message(BaseModel):
    sender: str
    text: str
    timestamp: int


class Metadata(BaseModel):
    channel: str
    language: str
    locale: str


class ScamRequest(BaseModel):
    sessionId: str
    message: Message
    conversationHistory: List = []
    metadata: Metadata


# -------- Scam Logic --------

def generate_reply(text: str) -> str:
    text = text.lower()

    if "verify" in text or "bank" in text:
        return "Why is my account being suspended?"

    if "money" in text or "upi" in text:
        return "Can you explain why payment is required?"

    return "I didn’t understand. Can you clarify?"


# -------- Endpoint --------

@app.post("/honeypot")
async def honeypot(
    request: ScamRequest,
    x_api_key: str = Header(...)
):

    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    reply = generate_reply(request.message.text)

    return {
        "status": "success",
        "reply": reply
    }
