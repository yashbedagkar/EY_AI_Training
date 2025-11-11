import streamlit as st
import requests

st.set_page_config(page_title="LangGraph Gemini Agent", layout="centered")

st.title("🤖 LangGraph Gemini Agent UI")
st.write("Ask me to add numbers, tell today's date, or reverse a word!")

BACKEND_URL = st.sidebar.text_input("Backend URL", value="http://127.0.0.1:8000/query")

query = st.text_input("Enter your query", value="", placeholder="e.g. add 5 and 7, or reverse constitution")
submit = st.button("Submit")

if submit:
    if not query.strip():
        st.error("Please type something!")
    else:
        with st.spinner("Thinking..."):
            try:
                resp = requests.post(BACKEND_URL, json={"query": query}, timeout=15)
                if resp.status_code == 200:
                    answer = resp.json().get("answer", "")
                    st.text_area("Answer", value=answer, height=120)
                else:
                    st.error(f"Backend error: {resp.text}")
            except Exception as e:
                st.error(f"Request failed: {e}")