from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import re

app = FastAPI()

# 🔐 API key (change this before deployment)
API_KEY = "XLENSAI_SECRET_123"


# ---------------------------
# Request Model
# ---------------------------
class ScamRequest(BaseModel):
    message: str
    history: list[str] = []


# ---------------------------
# Scam Detection Logic
# ---------------------------
def detect_scam(message: str):
    keywords = [
        "urgent", "bank", "otp", "verify", "suspend",
        "upi", "click", "account", "payment"
    ]
    return any(word in message.lower() for word in keywords)


# ---------------------------
# Intelligence Extraction
# ---------------------------
def extract_intelligence(text: str):

    upi = re.findall(r"\b[\w.-]+@[\w.-]+\b", text)
    urls = re.findall(r"https?://\S+", text)
    bank = re.findall(r"\b\d{9,18}\b", text)

    return {
        "upi_ids": upi,
        "bank_accounts": bank,
        "phishing_urls": urls
    }


# ---------------------------
# Agent Response Generator
# ---------------------------
def generate_agent_reply():

    replies = [
        "I didn’t understand. Can you explain?",
        "What should I do next?",
        "Please share more details.",
        "Is this urgent?",
        "Can you confirm the payment process?"
    ]

    import random
    return random.choice(replies)


# ---------------------------
# API Endpoint
# ---------------------------
@app.post("/honeypot")
def honeypot(
    data: ScamRequest,
    x_api_key: str = Header(None)
):

    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    scam_detected = detect_scam(data.message)

    extracted = extract_intelligence(data.message)

    agent_reply = generate_agent_reply() if scam_detected else None

    response = {
        "scam_detected": scam_detected,
        "agent_engaged": scam_detected,
        "agent_reply": agent_reply,
        "extracted_intelligence": extracted
    }

    return response
