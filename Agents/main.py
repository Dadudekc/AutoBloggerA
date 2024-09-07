from AgentCreator import AgentCreator

def main():
    # Initialize the agent creator with JSON configuration
    agent_creator = AgentCreator(json_config_file="agents_config.json")

    # Adding a new agent
    agent_creator.add_new_agent(
        name="SentimentAnalyzer",
        role="Sentiment Analysis",
        personality="You are an expert at analyzing social media and news sentiment.",
        task_keyword="sentiment_analysis",
        task_function="sentiment_analysis_function",
        additional_attributes={
            "tools": ["Twitter API", "News API"],
            "priority": 2
        }
    )
    print("New agent added.")

    # Editing an existing agent
    agent_creator.edit_agent(
        task_keyword="fetch",
        updates={"priority": 1, "max_requests_per_day": 1000}
    )
    print("Agent updated.")

    # Removing an agent
    agent_creator.remove_agent(task_keyword="journal")
    print("Agent removed.")

if __name__ == "__main__":
    main()
