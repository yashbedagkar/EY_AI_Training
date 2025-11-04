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
def count_words(sentence: str) -> str:
    """Count the number of words in a sentence."""
    words = sentence.split()
    count = len(words)
    return f"Your sentence has {count} words."

def reverse_text(sentence: str) -> str:
    """Reverse the order of words in a sentence."""
    words = sentence.split()
    reversed_sentence = " ".join(reversed(words))
    return reversed_sentence

def define_word(word: str) -> str:
    """Ask LLM for short definition"""
    prompt = f"Give a short definition for {word}"
    response = llm.invoke(prompt)
    return response.content.strip()

def change_case(text: str,mode:str) -> str:
    """Convert text to uppercase or lowercase"""
    if mode == "upper":
        return text.upper()
    elif mode == "lower":
        return text.lower()
    else:
        return "Invalid mode.Use upper or lower case"

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
        # Word Counter
        if user_input.lower().startswith("count"):
            text = user_input[len("count"):].strip()
            result = count_words(text)
            print("Agent:", result)
            memory.save_context({"input": user_input}, {"output": result})
            continue

        # Reverse Text
        if user_input.lower().startswith("reverse"):
            text = user_input[len("reverse"):].strip()
            result = reverse_text(text)
            print("Agent:", result)
            memory.save_context({"input": user_input}, {"output": result})
            continue

        # Vocabulary helper
        if user_input.lower().startswith("define"):
            text = user_input[len("define"):].strip()
            result = define_word(word=text)
            print("Agent:", result)
            memory.save_context({"input": user_input}, {"output": result})
            continue

        # Case Change
        if user_input.lower().startswith("upper"):
            text = user_input[len("upper"):].strip()
            result = change_case(text, "upper")
            print("Agent:", result)
            memory.save_context({"input": user_input}, {"output": result})
            continue

        if user_input.lower().startswith("lower"):
            text = user_input[len("lower"):].strip()
            result = change_case(text, "lower")
            print("Agent:", result)
            memory.save_context({"input": user_input}, {"output": result})
            continue

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

        #History
        if user_input.lower() == "history":
            history_data = memory.load_memory_variables({}).get("chat_history", [])
            if history_data:
                print("\n=== History Data ===")
                for i,msg in enumerate(history_data, 1):
                    print(f"{i}. {msg}")
            else:
                print("No history data")
            continue


        # Default: use LLM
        response = llm.invoke(user_input)
        print("Agent:", response.content)
        memory.save_context({"input": user_input}, {"output": response.content})

    except Exception as e:
        print("Error:", e)