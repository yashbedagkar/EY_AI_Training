# main.py
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
from typing import Any, Dict, List
import os, json, time
from datetime import datetime

# Load environment variables
load_dotenv()

# --- OpenRouter setup ---
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise RuntimeError("Missing OPENROUTER_API_KEY in .env")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

# Optional headers for analytics
OPENROUTER_HEADERS = {
    "HTTP-Referer": os.getenv("APP_URL", "http://localhost:8000"),
    "X-Title": os.getenv("APP_NAME", "FastAPI Mistral QnA App"),
}

# Free reliable model
DEFAULT_MODEL = "mistralai/mistral-7b-instruct"
# You can also try:
# DEFAULT_MODEL = "nousresearch/nous-capybara-7b"
# DEFAULT_MODEL = "openchat/openchat-7b"

app = FastAPI(title="Mistral Q&A via OpenRouter")

# --- Custom Exception Handler (422 → 400) ---
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

HISTORY_PATH = "qa_history.json"


# ---------- Pydantic Model ----------
class Prompt(BaseModel):
    topic: str
    question: str


# ---------- Helper Functions ----------
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


# ---------- Routes ----------
@app.get("/", response_class=HTMLResponse)
async def index():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<title>Mistral Q&A (Free via OpenRouter)</title>
<style>
body { font-family: system-ui; margin: 2rem; background: #f9fafb; color: #111; }
.card { max-width: 700px; margin: auto; background: white; padding: 2rem; border-radius: 1rem; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
h1 { margin-bottom: 1rem; }
label { font-weight: 600; margin-top: 1rem; display:block; }
input, textarea { width: 100%; padding: 0.75rem; margin-top: 0.5rem; border: 1px solid #d1d5db; border-radius: 8px; }
button { margin-top: 1rem; padding: 0.75rem 1.5rem; border: none; border-radius: 8px; background: #111827; color: white; cursor: pointer; }
button:hover { background: #1f2937; }
.answer { margin-top: 1rem; padding: 1rem; background: #f3f4f6; border-radius: 8px; white-space: pre-wrap; }
.error { color: #dc2626; margin-top: .5rem; }
#status { color: #6b7280; margin-top: 0.5rem; }
</style>
</head>
<body>
<div class="card">
  <h1>Ask Mistral (Free Model)</h1>
  <label>Topic:</label>
  <input id="topic" placeholder="e.g., Python, Nutrition, AI Ethics" />
  <label>Question:</label>
  <textarea id="question" rows="5" placeholder="Type your question here..."></textarea>
  <button id="askBtn">Ask</button>
  <div id="status"></div>
  <div id="answer" class="answer" style="display:none;"></div>
  <div id="error" class="error"></div>
</div>
<script>
  const btn = document.getElementById("askBtn");
  const topic = document.getElementById("topic");
  const question = document.getElementById("question");
  const status = document.getElementById("status");
  const answer = document.getElementById("answer");
  const errorBox = document.getElementById("error");

  btn.addEventListener("click", async () => {
    const t = topic.value.trim();
    const q = question.value.trim();
    status.textContent = "";
    errorBox.textContent = "";
    answer.style.display = "none";
    answer.textContent = "";
    if (!t || !q) {
      errorBox.textContent = "Both topic and question are required.";
      return;
    }

    status.textContent = "Thinking...";
    try {
      const res = await fetch("/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic: t, question: q }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Unknown error");
      answer.textContent = data.response;
      answer.style.display = "block";
      status.textContent = "Done.";
    } catch (err) {
      errorBox.textContent = "Error: " + err.message;
      status.textContent = "";
    }
  });
</script>
</body>
</html>
    """


@app.post("/generate")
async def generate_response(prompt: Prompt):
    # Manual validation for empty strings
    if not prompt.topic.strip():
        raise HTTPException(status_code=400, detail="Topic cannot be empty.")
    if not prompt.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    start = time.perf_counter()
    try:
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
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
            ],
            extra_headers=OPENROUTER_HEADERS,
        )

        # Extract answer safely
        answer = ""
        if response.choices:
            msg = response.choices[0].message
            if msg and msg.content and msg.content.strip():
                answer = msg.content.strip()

        # Fallback if blank
        if not answer:
            answer = (
                "Sorry, I couldn’t generate an answer for this question. "
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
