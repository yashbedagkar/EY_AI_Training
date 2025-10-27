import os
import json
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
# ----------------------------------------------------------
# 1. Load environment variables
# ----------------------------------------------------------
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
if not api_key:
   raise ValueError("OPENROUTER_API_KEY missing in .env")
# ----------------------------------------------------------
# 2. Initialize model (Mistral via OpenRouter)
# ----------------------------------------------------------
llm = ChatOpenAI(
   model="mistralai/mistral-7b-instruct",
   temperature=0.7,
   max_tokens=256,
   api_key=api_key,
   base_url=base_url,
)
# ----------------------------------------------------------
# 3. Define prompt templates
# ----------------------------------------------------------
summary_prompt = ChatPromptTemplate.from_template(
   "Summarize the topic '{topic}' in 3-4 simple lines for a beginner."
)
quiz_prompt = ChatPromptTemplate.from_template(
   "Generate 3 beginner-level quiz questions based on the topic '{topic}'. "
   "Do not provide answers."
)
parser = StrOutputParser()
# ----------------------------------------------------------
# 4. Define helper functions
# ----------------------------------------------------------
def generate_summary(topic):
   chain = summary_prompt | llm | parser
   return chain.invoke({"topic": topic})
def generate_quiz(topic):
   chain = quiz_prompt | llm | parser
   return chain.invoke({"topic": topic})
# ----------------------------------------------------------
# 5. Sequential execution
# ----------------------------------------------------------
topic = input("Enter a topic to summarize and generate quiz: ").strip()
# Step 1 — Generate Summary
summary = generate_summary(topic)
# Step 2 — Generate Quiz Questions
quiz = generate_quiz(topic)
# Step 3 — Display Results
print("\n--- SUMMARY ---")
print(summary)
print("\n--- QUIZ QUESTIONS ---")
print(quiz)
# ----------------------------------------------------------
# 6. Log results
# ----------------------------------------------------------
os.makedirs("logs", exist_ok=True)
log_entry = {
   "timestamp": datetime.utcnow().isoformat(),
   "topic": topic,
   "summary": summary,
   "quiz_questions": quiz
}
with open("logs/sequential_chain_log.jsonl", "a", encoding="utf-8") as f:
   f.write(json.dumps(log_entry) + "\n")
print("\nResults logged to logs/sequential_chain_log.jsonl")