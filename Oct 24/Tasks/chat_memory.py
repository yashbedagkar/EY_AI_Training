import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
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
   max_tokens=200,
   api_key=api_key,
   base_url=base_url,
)
# ----------------------------------------------------------
# 3. Chat with simple memory simulation
# ----------------------------------------------------------
def start_chat():
   print("=== Start Chatting with Memory ===")
   print("Type 'exit' to stop.\n")
   conversation_history = []
   while True:
       user_input = input("You: ").strip()
       if user_input.lower() == "exit":
           print("Conversation ended.")
           break
       # Build prompt with memory (previous chat)
       history_text = "\n".join(
           [f"You: {u}\nAssistant: {a}" for u, a in conversation_history]
       )
       prompt = f"""
The following is a friendly conversation between a human and an assistant.
The assistant remembers previous context and responds accordingly.
{history_text}
You: {user_input}
Assistant:"""
       response = llm.invoke(prompt)
       reply = response.content.strip()
       print(f"Assistant: {reply}\n")
       # Save memory
       conversation_history.append((user_input, reply))

# ----------------------------------------------------------
# 4. Run the chat
# ----------------------------------------------------------
if __name__ == "__main__":
   start_chat()