import sys
import os
import logging

# Initialize logging
logging.basicConfig(filename='/Auto_Blogger/Logs/main_log.log', level=logging.INFO)

# Set up dynamic path for the Agents directory
current_dir = os.path.dirname(os.path.abspath(__file__))
agents_dir = os.path.join(current_dir, 'Agents')
if agents_dir not in sys.path:
    sys.path.append(agents_dir)

from TaskManagerAgent import TaskManagerAgent
from AgentCreator import AgentCreator
from AgentVictor import AgentVictor
from DebuggerAgent import DebuggerAgent
from JournalAgent import JournalAgent

def main():
    """
    Main function to initialize the system and tie all agents together.
    """
    # Path to the configuration file for AgentCreator
    config_file = os.path.join(current_dir, 'config', 'agent_config.json')
    
    # Initialize AgentCreator to dynamically create agents from the config file
    agent_creator = AgentCreator(json_config_file=config_file)
    
    # Create a list of agents (add AgentVictor, DebuggerAgent, and JournalAgent manually)
    agent_registry = [
        AgentVictor(),
        DebuggerAgent(),
        JournalAgent()
    ]
    
    # Initialize TaskManagerAgent with the agent registry and agent creator
    task_manager = TaskManagerAgent(agent_registry, agent_creator)
    
    # Example tasks for the system to handle
    tasks = [
        "debug traceback error in the system",
        "journal the latest development session",
        "analyze trading strategy"
    ]
    
    # Assign tasks to the TaskManagerAgent
    for task in tasks:
        logging.info(f"Assigning task: {task}")
        result = task_manager.assign_task(task)
        logging.info(f"Result: {result}")
        print(f"Result: {result}")

def main():
    """
    Example usage of AgentVictor to populate general subordinates needed to run a company.
    """
    # Correct the configuration path to point to the actual location of agent_config.json
    config_file = os.path.join(current_dir, '../Scripts/config/agent_config.json')
    
    # Initialize AgentCreator with the json config file
    agent_creator = AgentCreator(json_config_file=config_file)
    
    # Initialize AgentVictor and the rest of the code here...

    main()
