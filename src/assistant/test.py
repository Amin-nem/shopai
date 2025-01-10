

db_file = "./conversation_history"
agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    # Store the memories and summary in a database
    memory=AgentMemory(
        db=SqliteMemoryDb(table_name="agent_memory", db_file=db_file), create_user_memories=True, create_session_summary=True
    ),
    # Store agent sessions in a database
    storage=SqlAgentStorage(table_name="personalized_agent_sessions", db_file=db_file),
    # Show debug logs so you can see the memory being created
    # debug_mode=True,
)

#
# if __name__ == "__main__":
#     # -*- Share personal information
#     agent.print_response("My name is john billings?", stream=True)
#     # -*- Print memories
#     pprint(agent.memory.memories)
#     # -*- Print summary
#     pprint(agent.memory.summary)
#
#     # -*- Share personal information
#     agent.print_response("I live in nyc?", stream=True)
#     # -*- Print memories
#     pprint(agent.memory.memories)
#     # -*- Print summary
#     pprint(agent.memory.summary)
#
#     # -*- Share personal information
#     agent.print_response("I'm going to a concert tomorrow?", stream=True)
#     # -*- Print memories
#     pprint(agent.memory.memories)
#     # -*- Print summary
#     pprint(agent.memory.summary)
#
#     # Ask about the conversation
#     agent.print_response("What have we been talking about, do you know my name?", stream=True)
#
#     agent.print_response("What was my last question?", stream=True)
#
