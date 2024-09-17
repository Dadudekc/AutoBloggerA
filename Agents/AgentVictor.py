import sys
import os
import importlib
import logging
import json

# Initialize logging
logging.basicConfig(filename='/Auto_Blogger/Logs/agent_victor_errors.log', level=logging.ERROR)

# Dynamically add the Agents directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
agents_dir = os.path.join(current_dir, 'Agents')
if agents_dir not in sys.path:
    sys.path.append(agents_dir)

# Import necessary classes
from GPT4Agent import GPT4Agent
from AgentCreator import AgentCreator
from TaskManagerAgent import TaskManagerAgent  # Import TaskManagerAgent


class AgentVictor(GPT4Agent):
    def __init__(self):
        super().__init__(
            name="AgentVictor",
            role="King",
            personality="Efficient, authoritative, and solution-oriented. I take responsibility for tasks, "
                        "but delegate where necessary and always expect results.",
            task_function=self.handle_task
        )
        self.agent_registry = []
        self.agent_creator = None  # Will be set by TaskManagerAgent

        # Explicitly set the correct path to the agent_config.json file
        self.config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../Scripts/config/agent_config.json')
        
        self.log_file = "/Auto_Blogger/Logs/agent_dialogue_log.txt"

    def add_subordinate(self, subordinate):
        """
        Adds a subordinate (new agent) to the config file.
        :param subordinate: A dictionary representing the subordinate's details.
        """
        # Load the existing config file
        with open(self.config_file, 'r') as file:
            config = json.load(file)

        # Add the new subordinate to the agents list in the config
        config['agents'].append(subordinate)

        # Save the updated config back to the file
        with open(self.config_file, 'w') as file:
            json.dump(config, file, indent=4)

        print(f"Subordinate {subordinate['name']} added to the configuration.")
    
    def handle_task(self, task_description):
        try:
            task_keywords = self.analyze_task(task_description)
            if task_keywords == "create model":
                return self.create_model_task()
            elif task_keywords == "debug":
                return self.debug_task(task_description)
            elif task_keywords == "journal":
                return self.journal_task(task_description)
            else:
                return self.command_agents(task_keywords, task_description)
        except Exception as e:
            self.self_heal(e)

    def create_model_task(self):
        """
        Handle the task of creating new agents (models) for autoblogging tasks.
        It also updates the agent_config.json file with the new model details.
        """
        new_agent = {
            "name": "AutobloggerModelAgent",
            "task_keyword": "autoblog",
            "role": "Autoblogging",
            "personality": "Expert in handling autoblogging tasks efficiently",
            "task_function": "autoblog_function"
        }

        # Load existing config
        with open(self.config_file, 'r') as file:
            config = json.load(file)

        # Add the new model to the agents list
        config['agents'].append(new_agent)

        # Save the updated config back to the file
        with open(self.config_file, 'w') as file:
            json.dump(config, file, indent=4)
        
        print(f"New model {new_agent['name']} added to the agent_config.json file.")
        return f"Model {new_agent['name']} created and added to the configuration."

    def debug_task(self, error_traceback):
        print(f"AgentVictor is fixing error: {error_traceback}")
        return f"Victor fixed the error: {error_traceback}"

    def journal_task(self, input_data):
        return f"Victor is writing a journal entry: {input_data}"

    def command_agents(self, task_keywords, task_description):
        assigned_agent = self.find_agent_for_task(task_keywords)
        if not assigned_agent:
            assigned_agent = self.agent_creator.create_agent(task_keywords)
            self.agent_registry.append(assigned_agent)
        
        result = assigned_agent.perform_task(task_description)
        self.log_dialogue(assigned_agent.name, task_description, result)
        return result

    def log_dialogue(self, agent_name, task_description, result):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"{timestamp} - {self.name} commanded {agent_name}: Task '{task_description}' resulted in: {result}\n"
        with open(self.log_file, 'a') as log:
            log.write(log_entry)

    def analyze_task(self, task_description):
        if "debug" in task_description.lower():
            return "debug"
        if "journal" in task_description.lower():
            return "journal"
        if "create model" in task_description.lower():
            return "create model"
        return "generic"

    def find_agent_for_task(self, task_keyword):
        for agent in self.agent_registry:
            if task_keyword in agent.role.lower():
                return agent
        return None

def main():
    """
    Example usage of AgentVictor to populate general subordinates needed to run a company.
    """
    # Correct the configuration path to point to the correct location
    config_file = os.path.join(current_dir, '../Scripts/config/agent_config.json')
    
    # Initialize AgentCreator with the json config file
    agent_creator = AgentCreator(json_config_file=config_file)
    
    # Initialize AgentVictor
    agent_victor = AgentVictor()

    # Add subordinates with essential company roles
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
        },
        {
            "name": "OperationsManager",
            "task_keyword": "manage operations",
            "role": "Operations",
            "personality": "Ensures smooth and efficient company operations",
            "task_function": "operations_management_function"
        },
        {
            "name": "MarketingManager",
            "task_keyword": "manage marketing",
            "role": "Marketing",
            "personality": "Responsible for overseeing marketing strategies and campaigns",
            "task_function": "marketing_management_function"
        }
    ]
    
    # AgentVictor will add these subordinates to the config
    for subordinate in subordinates:
        print(f"Creating subordinate: {subordinate['name']}")
        agent_victor.add_subordinate(subordinate)
    
    print("Subordinates added to agent_config.json.")

    # Assign tasks to subordinates through TaskManagerAgent
    task_manager = TaskManagerAgent([agent_victor], agent_creator)

    tasks = [
        "manage finances for the company",
        "recruit and manage employees",
        "oversee company operations",
        "launch marketing campaign"
    ]

    for task in tasks:
        result = task_manager.assign_task(task)
        print(f"Task result: {result}")

if __name__ == "__main__":
    main()
