import os
from dotenv import load_dotenv
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager

# ---------------------------------------------------------------------
# 1. Load environment variables
# ---------------------------------------------------------------------
load_dotenv()
os.environ["OPENROUTER_API_KEY"] = os.getenv("OPENROUTER_API_KEY")

# ---------------------------------------------------------------------
# 2. Define LLM Configuration for OpenRouter
# ---------------------------------------------------------------------
llm_config = {
    "model": "minimax/minimax-m2:free",
    "base_url": "https://openrouter.ai/api/v1",
    "api_key": os.getenv("OPENROUTER_API_KEY")
}

# ---------------------------------------------------------------------
# 3. Define Agents
# ---------------------------------------------------------------------
planner = AssistantAgent(
    name="planner",
    llm_config=llm_config,
    system_message="You are a strategic planner. Create a 3-step plan with goals and deliverables for the given topic."
)

specialist = AssistantAgent(
    name="specialist",
    llm_config=llm_config,
    system_message="You are a specialist who executes plans. Summarize the results of each step clearly."
)

user_proxy = UserProxyAgent(
    name="user_proxy",
    code_execution_config={"use_docker": False}
)

# ---------------------------------------------------------------------
# 4. Define Group Chat and Manager
# ---------------------------------------------------------------------
group_chat = GroupChat(agents=[planner, specialist, user_proxy], messages=[], max_round=5)
manager = GroupChatManager(groupchat=group_chat, llm_config=llm_config)

# ---------------------------------------------------------------------
# 5. Run the Workflow
# ---------------------------------------------------------------------
if __name__ == "__main__":
    topic = "Developing an AI-based document summarization system"
    print(f"\n--- Running AutoGen Planner–Specialist Workflow ---\nTopic: {topic}\n")
    user_proxy.initiate_chat(manager, message=f"Create and execute a plan for: {topic}")
