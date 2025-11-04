# ============================================================
# Memory-Tools.py — Conversational Mistral Agent (fully working)
# ============================================================

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory


# ------------------------------------------------------------
# 1. Load environment variables
# ------------------------------------------------------------
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY not found in .env file")


# ------------------------------------------------------------
# 2. Initialize the Mistral model via OpenRouter
# ------------------------------------------------------------
llm = ChatOpenAI(
    model="google/gemma-3n-e4b-it:free",
    temperature=0.4,
    max_tokens=512,
    api_key=api_key,
    base_url=base_url,
)


# ------------------------------------------------------------
# 3. Define helper tools
# ------------------------------------------------------------
def repeat_word(word:str, times:int) -> str:
    """Repeat a word a specified number of times."""
    try:
        times = int(times)
        return " ".join([word] * times)
    except ValueError:
        return "Please specify a number of times"


# ------------------------------------------------------------
# 4. Initialize memory
# ------------------------------------------------------------
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)


# ------------------------------------------------------------
# 5. Conversational loop
# ------------------------------------------------------------
print("\n=== Start chatting with your Agent ===")
print("Type 'exit' to quit.\n")

while True:
    user_input = input("You: ").strip()
    if user_input.lower() == "exit":
        print("\nConversation ended.")
        break

    try:
        #Word Repeater
        if user_input.lower().startswith("repeat"):
            parts = user_input.split()
            if len(parts) >= 3:
                word = parts[1]
                times = parts[2]
                result = repeat_word(word, times)
            else:
                result = "Usage: repeat_word <word> <number>"
            print("Agent:", result)
            memory.save_context({"input": user_input}, {"output": result})
            continue


        # Default: use LLM
        response = llm.invoke(user_input)
        print("Agent:", response.content)
        memory.save_context({"input": user_input}, {"output": response.content})

    except Exception as e:
        print("Error:", e)