# ============================================================
# CrewAI Demo — Mistral via OpenRouter API
# ============================================================

from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

# ------------------------------------------------------------
# 1. Load Environment Variables
# ------------------------------------------------------------
load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

if not api_key:
    raise ValueError("❌ Missing OPENROUTER_API_KEY in .env")

# ------------------------------------------------------------
# 2. Initialize Mistral Model from OpenRouter
# ------------------------------------------------------------
# Important: Prefix model with "openrouter/"
llm = ChatOpenAI(
    model="openrouter/mistralai/mistral-7b-instruct",  # ✅ Correct model format
    temperature=0.7,
    api_key=api_key,
    base_url=base_url,
)

# ------------------------------------------------------------
# 3. Ask for Topic
# ------------------------------------------------------------
topic = input("Enter a topic to research: ")

# ------------------------------------------------------------
# 4. Create Agent
# ------------------------------------------------------------
researcher = Agent(
    role="AI Research Assistant",
    goal="Research the given topic and summarize key findings.",
    backstory="You are a skilled analyst specializing in summarizing complex topics clearly.",
    llm=llm
)

# ------------------------------------------------------------
# 5. Create Task (make sure expected_output is included)
# ------------------------------------------------------------
task = Task(
    description=f"Research and summarize the latest insights about: {topic}",
    expected_output="A clear, concise, and well-structured summary in paragraph form.",
    agent=researcher
)

# ------------------------------------------------------------
# 6. Create Crew and Run
# ------------------------------------------------------------
crew = Crew(
    agents=[researcher],
    tasks=[task],
    verbose=True
)

print("\n🔍 Researching... please wait...\n")
result = crew.kickoff()

# ------------------------------------------------------------
# 7. Display Result
# ------------------------------------------------------------
print("\n🧠 Research Summary:\n")
print(result)
