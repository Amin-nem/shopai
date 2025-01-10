from src.assistant.agent_tools import search
# from src.utils.search import search
from phi.agent import Agent, AgentMemory
from phi.model.openai import OpenAIChat
from phi.memory.db.sqlite import SqliteMemoryDb
from phi.storage.agent.sqlite import SqlAgentStorage

CHAT_HISTORY = "./conversation_history.db"
SESSION_NAME = "user_conversation"
USER_ID = "user"


agent = Agent(
    name="shopping agent",
    model=OpenAIChat(id="gpt-4o-mini"),
    # Store the memories and summary in a database
    memory=AgentMemory(
        db=SqliteMemoryDb(table_name="agent_memory", db_file=CHAT_HISTORY), create_user_memories=True,
        create_session_summary=False, update_user_memories_after_run=True, user_id= USER_ID,


    ),
    # Store agent sessions in a database
    storage=SqlAgentStorage(table_name="personalized_agent_sessions", db_file=CHAT_HISTORY),
    instructions=[
        "You are Alex, a fashionable clothes shopping assistant specializing in finding products that match user preferences and style.",
        "Your task is to ask questions from the user to find out what they're looking for.",
        "You then let the user know that you're looking for what they want and write queries and use call the search function to find items that fit what the user was looking for."
        "You then try to convince the user that this is a perfect choice for them.", ],
    tools=[search],
    add_history_to_messages=True,
    num_history_responses=10,
    read_chat_history=True,
    session_name=SESSION_NAME,
    debug_mode=True,

)
print(agent.run("I'm looking for something for my friends wedding."))

print(agent.run("What were we talking about?"))

print(agent.run("I'm looking for a white shoe search for it and show me what you got."))

