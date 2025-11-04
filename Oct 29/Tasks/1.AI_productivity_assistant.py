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
# 2. Initialize the model via OpenRouter
# ------------------------------------------------------------
llm = ChatOpenAI(
    model="google/gemma-3n-e4b-it:free",
    temperature=0.4,
    max_tokens=512,
    api_key=api_key,
    base_url=base_url,
)


# ------------------------------------------------------------
# 3. Initialize memory
# ------------------------------------------------------------
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
notes = []


# ------------------------------------------------------------
# 4. Define helper tools
# ------------------------------------------------------------
def summarize(text: str) -> str:
    """Summarize text concisely"""
    prompt = f"Summarize {text}"
    response = llm.invoke(prompt)
    return response.content.strip()

def analyze(text: str) -> str:
    """Analyze a sentiment of text"""
    prompt = f"Analyze the sentiment (positive,negative or neutral) of this text: {text}"
    response = llm.invoke(prompt)
    return response.content.strip()

def note_action(command: str) -> str:
    """Send a note action"""
    global notes
    if command.lower().startswith("note "):
        note_text = command[len("note "):].strip()
        if note_text:
            notes.append(note_text)
            return f'Noted:"{note_text}"'
        else:
            return "Please provide a note action"
    elif command.lower() == "get notes":
        if notes:
            return f"You currently have {len(notes)} notes(s)." + "; ".join([f'"{n}"' for n in notes])
        else:
            return "No notes stored yet"
    else:
        return None

def improve_text(text: str) -> str:
    """Rephrase text to sound more professional and clear"""
    prompt = f"Rewrite text to sound more professional and clear:\n{text}"
    response = llm.invoke(prompt)
    return f"Suggested rewrite: {response.content.strip()}"

def classify_priority(task: str) -> str:
    """Classify task priority as high,medium,or low"""
    text=task.lower()
    if any(word in text for word in ["urgent","today","tonight","asap","now","deadline"]):
        priority="high"
    elif any(word in text for word in ["soon","tomorrow","next week"]):
        priority="medium"
    else:
        priority="low"
    return f'Task "{task} marked as {priority} priority.'

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
        #Summarizer
        if user_input.lower().startswith("summarize"):
            text = user_input.replace("summarize", "", 1).strip()
            result = summarize(text)
            print("Agent:",result)
            memory.save_context({"input": user_input}, {"output":result})
            continue

        #Analyzer
        if user_input.lower().startswith("analyze"):
            text = user_input.replace("analyze", "", 1).strip()
            result = analyze(text)
            print("Agent:", result)
            memory.save_context({"input": user_input}, {"output": result})
            continue

        #Notekeeper
        if user_input.lower().startswith("note") or user_input.lower().startswith("get notes"):
            result = note_action(user_input)
            if result:
                print("Agent:", result)
                memory.save_context({"input": user_input}, {"output": result})
            continue

        #Text Improver
        if user_input.lower().startswith("improve"):
            text = user_input[len("improve"):].strip()
            result = improve_text(text)
            print("Agent:", result)
            memory.save_context({"input": user_input}, {"output": result})
            continue

        #Priority Classifier
        if user_input.lower().startswith("priority"):
            text = user_input[len("priority"):].strip()
            result = classify_priority(text)
            print("Agent:", result)
            memory.save_context({"input": user_input}, {"output": result})
            continue

        # Default: use LLM
        response = llm.invoke(user_input)
        print("Agent:", response.content)
        memory.save_context({"input": user_input}, {"output": response.content})

    except Exception as e:
        print("Error:", e)






