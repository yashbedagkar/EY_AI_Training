"""
RAG Chatbot with Persistent Session Memory (Reset on Exit)

- Keeps full memory during one chat session.
- Clears memory and exits completely when user types 'exit' or 'bye'.
"""

import os
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import GoogleGenerativeAI
from retriever import load_retriever, build_context
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def build_chatbot(memory):
    """
    Builds a RAG chatbot pipeline with retriever, LLM, and chat memory.
    """
    os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

    llm = GoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)
    retriever = load_retriever(index_name="budget_faiss_index", k=6)

    # The main prompt that forces grounding in context
    prompt_template = PromptTemplate(
        input_variables=["context", "chat_history", "question"],
        template="""
You are a Budget Analysis Assistant that answers ONLY using the provided CONTEXT and chat history.

If the answer cannot be found in the CONTEXT, respond exactly with:
"I don't know — the provided documents don't contain the information needed to answer that."

CHAT HISTORY:
{chat_history}

CONTEXT:
{context}

QUESTION:
{question}

Rules:
- Use only the CONTEXT and chat history.
- Do NOT use outside knowledge.
- If answering, provide a short 3–4 sentence answer.
"""
    )

    # Function to dynamically build context and inject memory
    def prepare_inputs(inputs):
        question = inputs["question"]

        # Get past chat history
        chat_history_str = "\n".join(
            [f"User: {m.content}" if m.type == "human" else f"Assistant: {m.content}"
             for m in memory.chat_memory.messages]
        )

        # Retrieve relevant documents
        docs = retriever.invoke(question)
        context = build_context(docs)

        return {"context": context, "chat_history": chat_history_str, "question": question}

    parser = StrOutputParser()
    main_chain = RunnableLambda(prepare_inputs) | prompt_template | llm | parser
    return main_chain


def start_chat():
    """
    Starts a persistent chat session that remembers context until 'exit' is typed.
    """
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    main_chain = build_chatbot(memory)

    print("\n===================================")
    print("  💬 Budget Chatbot (type 'exit' or 'bye' to quit)")
    print("===================================\n")

    while True:
        user_input = input(" You: ").strip()

        # Exit condition
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("\n🧹 Clearing chat memory...")
            memory.clear()
            print("👋 Chat ended. Goodbye!\n")
            break

        # Get response
        response = main_chain.invoke({"question": user_input})

        # Store conversation turns in memory
        memory.chat_memory.add_user_message(user_input)
        memory.chat_memory.add_ai_message(response)

        print("\n Bot:", response, "\n")


if __name__ == "__main__":
    start_chat()
