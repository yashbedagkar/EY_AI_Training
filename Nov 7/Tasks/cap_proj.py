from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import Any, Dict, List
import os
import json
import time
import requests
from datetime import datetime

# Loading environment variables
load_dotenv()

# OpenRouter setup
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise RuntimeError("Missing OPENROUTER_API_KEY in .env")

# OpenRouter Configuration
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": os.getenv("APP_URL", "http://localhost:8000"),
    "X-Title": os.getenv("APP_NAME", "FastAPI Mistral QnA App"),
}


DEFAULT_MODEL = "mistralai/mistral-7b-instruct"
# DEFAULT_MODEL = "meta-llama/llama-3-8b-instruct"
# DEFAULT_MODEL = "google/gemini-flash-1.5"

app = FastAPI(title="Mistral Q&A via OpenRouter")


# Custom Exception Handler (422 → 400)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        loc = " → ".join(str(x) for x in err.get("loc", []))
        msg = err.get("msg", "")
        errors.append(f"{loc}: {msg}")
    return JSONResponse(
        status_code=400,
        content={
            "detail": "Invalid input. Ensure 'topic' and 'question' are provided.",
            "errors": errors,
        },
    )


HISTORY_PATH = "qa_history_proj.json"


# Pydantic Model
class Prompt(BaseModel):
    topic: str
    question: str


# Helper Functions
def _read_history() -> List[Dict[str, Any]]:
    if not os.path.exists(HISTORY_PATH):
        return []
    try:
        with open(HISTORY_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        ts = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        os.rename(HISTORY_PATH, f"{HISTORY_PATH}.bak.{ts}")
        return []


def _append_history(entry: Dict[str, Any]) -> None:
    data = _read_history()
    data.append(entry)
    with open(HISTORY_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# Routes
@app.post("/generate")
async def generate_response(prompt: Prompt):
    # Manual validation for empty strings
    if not prompt.topic.strip():
        raise HTTPException(status_code=400, detail="Topic cannot be empty.")
    if not prompt.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    start = time.perf_counter()

    # Construct payload for OpenRouter
    payload = {
        "model": DEFAULT_MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a knowledgeable and helpful AI assistant. "
                    "Always provide a clear, complete answer to the user's question. "
                    "If unsure, say 'I'm not certain, but here's what I know.'"
                ),
            },
            {
                "role": "user",
                "content": f"Topic: {prompt.topic}\nQuestion: {prompt.question}"
            }
        ]
    }

    try:
        # Making POST request to OpenRouter
        response = requests.post(
            OPENROUTER_BASE_URL,
            headers=OPENROUTER_HEADERS,
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        data = response.json()

        # Extracting answer from choices[0].message.content
        answer = ""
        if "choices" in data and len(data["choices"]) > 0:
            choice = data["choices"][0]
            if "message" in choice and "content" in choice["message"]:
                answer = choice["message"]["content"].strip()

        # Fallback if blank
        if not answer:
            answer = (
                "Sorry, I couldn't generate an answer for this question. "
                "Try rephrasing it or being more specific."
            )

        elapsed = round(time.perf_counter() - start, 3)

        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "model": DEFAULT_MODEL,
            "topic": prompt.topic,
            "question": prompt.question,
            "answer": answer,
            "latency_sec": elapsed,
        }
        _append_history(entry)
        return {"response": answer}

    except Exception as e:
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "model": DEFAULT_MODEL,
            "topic": prompt.topic,
            "question": prompt.question,
            "error": str(e),
        }
        _append_history(entry)
        raise HTTPException(status_code=500, detail=f"Generation failed: {e}")


@app.get("/history")
async def get_history():
    return _read_history()