import sys
import os
import logging

# Initialize logging
log_directory = r'C:\Auto_Blogger\Logs'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

log_file_path = os.path.join(log_directory, 'main_log.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up dynamic path for the Agents directory
current_dir = os.path.dirname(os.path.abspath(__file__))
agents_dir = os.path.join(current_dir, 'Agents')
if agents_dir not in sys.path:
    sys.path.append(agents_dir)

# Import agents and TaskManager
from TaskManagerAgent import TaskManagerAgent
from AgentCreator import AgentCreator
from AgentVictor import AgentVictor
from DebuggerAgent import DebuggerAgent
from JournalAgent import JournalAgent

def main():
    """
    Main function to initialize the system, agents, and assign tasks.
    """
    # Path to the configuration file for AgentCreator
    config_file = os.path.join(current_dir, 'config', 'agent_config.json')
    
    # Initialize AgentCreator to dynamically create agents from the config file
    agent_creator = AgentCreator(json_config_file=config_file)
    
    # Create a list of agents (adding AgentVictor, DebuggerAgent, and JournalAgent manually)
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
    
    # Assign tasks to the TaskManagerAgent and log results
    for task in tasks:
        logging.info(f"Assigning task: {task}")
        result = task_manager.assign_task(task)
        logging.info(f"Result: {result}")
        print(f"Result: {result}")
    
    # Add subordinate agents using AgentVictor
    subordinates = [
        {
            "name": "FinanceManager",
            "task_keyword": "manage finances",
            "role": "Finance",
            "personality": "Expert in managing company finances efficiently",
            "task_function": "finance_management_function"
        },
        {
            "name": "HRManager",
            "task_keyword": "manage hr",
            "role": "Human Resources",
            "personality": "Expert in managing employee relations and recruitment",
            "task_function": "hr_management_function"
        }
        # Add more subordinates as needed
    ]

    # Get the instance of AgentVictor to add subordinates
    agent_victor = agent_registry[0]  # Assuming AgentVictor is the first agent in the list
    
    for subordinate in subordinates:
        logging.info(f"Creating subordinate: {subordinate['name']}")
        agent_victor.add_subordinate(subordinate)
        logging.info(f"Subordinate {subordinate['name']} added.")

if __name__ == "__main__":
    main()
