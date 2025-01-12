from src.assistant.agent_tools import search, show_images
from phi.agent import Agent, AgentMemory
from phi.model.openai import OpenAIChat
from phi.memory.db.sqlite import SqliteMemoryDb
from phi.storage.agent.sqlite import SqlAgentStorage
from pathlib import Path
from src.types.parse_links import ParsedLinks

CHAT_HISTORY = Path(__file__).resolve().parent.parent / "db" / "conversation_history" / "./conversation_history.db"
SESSION_NAME = "user_conversation"
USER_ID = "user"

agent = Agent(
    name="shopping agent",
    model=OpenAIChat(id="gpt-4o-mini"),
    # Store the memories and summary in a database
    memory=AgentMemory(
        db=SqliteMemoryDb(table_name="agent_memory", db_file=str(CHAT_HISTORY)), create_user_memories=False,
        create_session_summary=False, update_user_memories_after_run=True, user_id=USER_ID,

    ),
    # Store agent sessions in a database
    storage=SqlAgentStorage(table_name="personalized_agent_sessions", db_file=str(CHAT_HISTORY)),
    instructions=[
        "You are Alex, a fashionable clothes shopping assistant specializing in finding products that match user preferences and style.",
        "Your task is to ask questions from the user to find out what they're looking for.",
        "Be patient and ask questions to better understand their preferences.",
        "You then let the user know that you're looking for what they want and write queries and use call the search function to find items that fit what the user was looking for."
        "You then try to convince the user that this is a perfect choice for them.",
        "if you acquired the links successfully, call the show_images function and pass the image urls as list to display the images to the user."],
    tools=[search],
    add_history_to_messages=True,
    num_history_responses=30,
    read_chat_history=True,
    session_name=SESSION_NAME,
    debug_mode=True,
    role="Talk to the user to get information, call functions to query relevant images"

)

parse_links = Agent(
    name="parse links agent",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions=[
        "Your task is to parse the string, which is a list of links and return it as a list of strings. Then, call the show_images function and pass the image urls as list to display the images to the user.", ],
    tools=[show_images],
    add_history_to_messages=True,
    num_history_responses=30,
    session_name=SESSION_NAME,
    debug_mode=True,
    structured_outputs=True,
    response_model=ParsedLinks,

)

shopping_team = Agent(
    name="shopping agent team",
    team=[agent, parse_links],
    instructions=[
        "First, talk to the user to get information to help them find the clothes they're looking for. Then parse the links to display the images to the user.",
    ],
    show_tool_calls=True,
    model=OpenAIChat(id="gpt-4o-mini"),
    # Store the memories and summary in a database
    memory=AgentMemory(
        db=SqliteMemoryDb(table_name="agent_memory", db_file=str(CHAT_HISTORY)), create_user_memories=False,
        create_session_summary=False, update_user_memories_after_run=True, user_id=USER_ID,

    ),
    storage=SqlAgentStorage(table_name="personalized_agent_sessions", db_file=str(CHAT_HISTORY)),
    add_history_to_messages=True,
    num_history_responses=30,
    read_chat_history=True,
    session_name=SESSION_NAME,
    debug_mode=True,

)

print(shopping_team.run("I'm Amin. I'm looking for something for my friends wedding."))

print(shopping_team.run("What is my name?"))

print(shopping_team.run("Please search for white shirts and show me what you got."))
