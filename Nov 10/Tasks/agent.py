import os
import logging
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langgraph.graph import StateGraph, START, END
from typing import TypedDict
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('agent.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env file")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"],
                   allow_headers=["*"])


class AgentState(TypedDict):
    messages: list
    decision: dict
    answer: str


def add_numbers(a: float, b: float) -> str:
    result = a + b
    return f"The sum is: {int(result) if result.is_integer() else result}"


def get_today_date() -> str:
    now = datetime.now()
    return f"Today's date is {now.strftime('%A, %B %d, %Y')}."


def reverse_word(word: str) -> str:
    return f"The reversed word is: {word[::-1]}"


def llm_step(state: AgentState):
    user_query = state["messages"][-1]["content"]

    prompt = f"""Analyze: "{user_query}"

Reply ONLY with one of these exact formats:
- add_numbers|5|7
- get_today_date
- reverse_word|hello
- none

No extra text."""

    try:
        response = model.generate_content(prompt)
        output = response.text.strip().lower()
        logger.info(f"Query: {user_query} | Gemini: {output}")

        decision = {"tool": "none", "args": {}}

        if "add_numbers" in output and "|" in output:
            parts = output.split("|")
            if len(parts) >= 3:
                decision = {"tool": "add_numbers", "args": {"a": float(parts[1]), "b": float(parts[2])}}
        elif "get_today_date" in output:
            decision = {"tool": "get_today_date", "args": {}}
        elif "reverse_word" in output and "|" in output:
            parts = output.split("|")
            if len(parts) >= 2:
                decision = {"tool": "reverse_word", "args": {"word": parts[1].strip()}}

        return {"decision": decision}
    except Exception as e:
        logger.error(f"Error: {e}")
        return {"decision": {"tool": "none", "args": {}}}


def tool_step(state: AgentState):
    decision = state.get("decision", {})
    tool = decision.get("tool")
    args = decision.get("args", {})

    if tool == "add_numbers":
        result = add_numbers(**args)
    elif tool == "get_today_date":
        result = get_today_date()
    elif tool == "reverse_word":
        result = reverse_word(**args)
    else:
        result = "Sorry, I can only add numbers, tell today's date, or reverse a word."

    return {"answer": result}


graph = StateGraph(AgentState)
graph.add_node("llm_step", llm_step)
graph.add_node("tool_step", tool_step)
graph.add_edge(START, "llm_step")
graph.add_edge("llm_step", "tool_step")
graph.add_edge("tool_step", END)
agent = graph.compile()


class QueryRequest(BaseModel):
    query: str


@app.post("/query")
async def query_endpoint(req: QueryRequest):
    try:
        result = agent.invoke({"messages": [{"role": "user", "content": req.query}]})
        return {"answer": result.get("answer", "Error processing request")}
    except Exception as e:
        logger.error(f"Error: {e}")
        return {"answer": "Error processing request"}


@app.get("/")
async def root():
    return {"message": "Agent running"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("agent:app", host="127.0.0.1", port=8000, reload=False)