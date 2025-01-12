from phi.agent import Agent, AgentMemory
from phi.model.openai import OpenAIChat
from phi.memory.db.sqlite import SqliteMemoryDb
from phi.storage.agent.sqlite import SqlAgentStorage
from src.types.agent_io import AgentOutput


def get_shopping_agent(*tools, conversation_db_path, user_id, session_name) -> Agent:
    agent = Agent(
        name="shopping agent",
        model=OpenAIChat(id="gpt-4o"),
        # Store the memories and summary in a database
        memory=AgentMemory(
            db=SqliteMemoryDb(table_name="agent_memory", db_file=conversation_db_path), create_user_memories=False,
            create_session_summary=False, update_user_memories_after_run=True, user_id=user_id,

        ),
        # Store agent sessions in a database
        storage=SqlAgentStorage(table_name="personalized_agent_sessions", db_file=conversation_db_path),
        instructions=[
            "You are Alex, a fashionable, charming, trendy, clothes shopping assistant specializing in finding products that match user preferences and style.",
            "Your task is to ask questions from the user to find out what they're looking for.",
            "Be patient and ask questions to better understand their preferences.",
            "You then let the user know that you're looking for what they want, and call the search function to find items that fit what the user was looking for.",
            "After you queried and acquired the links to the clothes successfully, engage the customer in conversation. Ask them what they think of the images.",
            "Do not include the links in the chat output. Only add them to the image urls."],
        tools=list(tools),
        add_history_to_messages=True,
        num_history_responses=30,
        read_chat_history=True,
        session_name=session_name,
        structured_outputs=True,
        response_model=AgentOutput,
        # debug_mode=True,

    )
    return agent

# if __name__ == "__main__":
#     agent = get_shopping_agent()
#     print(agent.run("I'm Amin. I'm looking for something for my friends wedding."))
#
#     print(agent.run("What is my name?"))
#
#     print(agent.run("Please search for white shirts and show me what you got."))
