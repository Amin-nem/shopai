from src.assistant.agent_tools import search, show_images
from phi.agent import Agent, AgentMemory
from phi.model.openai import OpenAIChat
from phi.memory.db.sqlite import SqliteMemoryDb
from phi.storage.agent.sqlite import SqlAgentStorage
from pathlib import Path

CHAT_HISTORY = Path(__file__).resolve().parent.parent / "db" / "conversation_history" / "./conversation_history.db"
SESSION_NAME = "user_conversation"
USER_ID = "user"

agent = Agent(
    name="shopping agent",
    model=OpenAIChat(id="gpt-4o-mini"),
    # Store the memories and summary in a database
    memory=AgentMemory(
        db=SqliteMemoryDb(table_name="agent_memory", db_file=CHAT_HISTORY), create_user_memories=False,
        create_session_summary=False, update_user_memories_after_run=True, user_id=USER_ID,

    ),
    # Store agent sessions in a database
    storage=SqlAgentStorage(table_name="personalized_agent_sessions", db_file=CHAT_HISTORY),
    instructions=[
        "You are Alex, a fashionable clothes shopping assistant specializing in finding products that match user preferences and style.",
        "Your task is to ask questions from the user to find out what they're looking for.",
        "Be patient and ask questions to better understand their preferences.",
        "You then let the user know that you're looking for what they want and write queries and use call the search function to find items that fit what the user was looking for.",
        "After you queried and acquired the links to the clothes successfully, call the show_images function and pass the image urls in this format: \"[\"https://image.jpg\",\"https//image2.jpg\"]\"as list to display the images to the user. This will show the images to the user. So you don't need to send the links to the user directly."
        "Then try to engage the customer in conversation. Ask them what they think of the images (remember: user will see the images, so don't show them the links. The links should only be sent to the show_images function in the format specified)."],
    tools=[search, show_images],
    add_history_to_messages=True,
    num_history_responses=30,
    read_chat_history=True,
    session_name=SESSION_NAME,
    #debug_mode=True,

)

print(agent.run("I'm Amin. I'm looking for something for my friends wedding."))

print(agent.run("What is my name?"))

print(agent.run("Please search for white shirts and show me what you got."))
