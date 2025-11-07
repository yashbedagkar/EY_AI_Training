import streamlit as st
import uuid
from crew_agent import handle_user_query
from langchain.memory import ConversationBufferMemory

# -----------------------------
# Streamlit Page Config
# -----------------------------
st.set_page_config(page_title="India's Budget AI Agent", page_icon="💰", layout="centered")
st.title("💰 India's Union Budget & Economy AI Agent Assistant")
st.caption("Ask anything about the Union Budgets or India's Economy — An intelligent Gemini-powered agent that can chat, calculate, visualize, or fetch real-time info.")

# -----------------------------
# Session State Setup
# -----------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.header("🧭 Controls")
    if st.button("🔄 End Chat"):
        st.session_state.chat_history = []
        st.session_state.memory.clear()
        st.success("Chat history cleared!")

    st.markdown("---")
    st.markdown("💬 **Ask questions like:**")
    st.markdown("- What is the fiscal deficit for year 2025–26?")
    st.markdown("- What is the role of RBI in the economy?")
    st.markdown("- Visualize the custom duty rate changes in chemicals commodity in budget 2025-26")
    st.markdown("- Visualize India's GDP growth in from 2021 to 2024")
    st.markdown(f"- Calculate 15% of 76000")

# -----------------------------
# Chat Display
# -----------------------------
for message in st.session_state.chat_history:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message.get('content', ''))

    elif message["role"] == "agent":
        with st.chat_message("assistant"):
            # Display the text content
            st.markdown(message.get('content', ''))
            
            # If there's a visualization, display it
            if message.get("type") == "visualization" and message.get("figure"):
                st.plotly_chart(
                    message["figure"],
                    use_container_width=True,
                    key=message.get("key", f"plot_{uuid.uuid4().hex[:8]}")
                )

# -----------------------------
# User Input Area
# -----------------------------
user_input = st.chat_input("Ask your question about the budget...")

if user_input:
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Process the query using the orchestrator agent
    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking..."):
            response = handle_user_query(user_input)

        # Handle response based on type
        if isinstance(response, dict):
            response_type = response.get("type", "text")
            response_content = response.get("content", "")
            
            # Display text content
            st.markdown(response_content)
            
            # If visualization, display the chart
            if response_type == "visualization" and response.get("figure"):
                st.plotly_chart(
                    response["figure"],
                    use_container_width=True,
                    key=response.get("key", f"plot_{uuid.uuid4().hex[:8]}")
                )
                
                # Store visualization response
                st.session_state.chat_history.append({
                    "role": "agent",
                    "type": "visualization",
                    "content": response_content,
                    "figure": response.get("figure"),
                    "key": response.get("key", f"plot_{uuid.uuid4().hex[:8]}")
                })
            else:
                # Store text-only response
                st.session_state.chat_history.append({
                    "role": "agent",
                    "type": "text",
                    "content": response_content
                })
        else:
            # Handle string responses (backward compatibility)
            st.markdown(str(response))
            st.session_state.chat_history.append({
                "role": "agent",
                "type": "text",
                "content": str(response)
            })

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.caption("💡 Powered by Gemini + RAG + CrewAI + Dynamic Visualization ")