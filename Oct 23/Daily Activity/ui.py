import os
from dotenv import load_dotenv
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# 1. Load environment variables
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

if not api_key:
    st.error("OPENROUTER_API_KEY not found in .env file")

# 2. Streamlit app UI
st.title("OpenRouter LLaMA Chat UI")

system_msg = st.text_area("System Message", "You are a helpful and concise AI assistant.")
user_msg = st.text_area("User Query", "Explain convolutional neural networks in simple terms.")

if st.button("Submit"):
    if not user_msg.strip():
        st.warning("Please enter a user query.")
    else:
        # 3. Initialize LangChain LLM
        llm = ChatOpenAI(
            model="meta-llama/llama-4-maverick:free",  # free model
            temperature=0.7,
            max_tokens=256,
            api_key=api_key,
            base_url=base_url,
        )

        messages = [
            SystemMessage(content=system_msg),
            HumanMessage(content=user_msg),
        ]

        try:
            response = llm.invoke(messages)
            st.subheader("Assistant Response:")
            st.write(response.content.strip() or "(no content returned)")
        except Exception as e:
            st.error(f"Error: {e}")
