import sys
import os
import importlib
import logging

# Initialize logging
logging.basicConfig(filename='/Auto_Blogger/Logs/agent_victor_errors.log', level=logging.ERROR)

# Dynamically add the Agents directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
agents_dir = os.path.join(current_dir, 'Agents')
if agents_dir not in sys.path:
    sys.path.append(agents_dir)

# Try importing GPT4Agent after dynamically adjusting sys.path
from GPT4Agent import GPT4Agent  # Import the GPT4Agent class


class AgentVictor(GPT4Agent):
    def __init__(self):
        super().__init__(
            name="AgentVictor",
            role="King",
            personality="Efficient, authoritative, and solution-oriented. I take responsibility for tasks, "
                        "but delegate where necessary and always expect results."
        )
        self.agent_registry = []
        self.agent_creator = None  # Will be set by TaskManagerAgent
        self.log_file = "/Auto_Blogger/Logs/agent_dialogue_log.txt"

    def handle_task(self, task_description):
        try:
            task_keywords = self.analyze_task(task_description)
            if task_keywords == "debug":
                return self.debug_task(task_description)
            elif task_keywords == "journal":
                return self.journal_task(task_description)
            else:
                return self.command_agents(task_keywords, task_description)
        except Exception as e:
            self.self_heal(e)
    
    def self_heal(self, error):
        error_type = type(error).__name__
        logging.error(f"AgentVictor encountered an error: {error_type} - {error}")
        if error_type == "NameError":
            self.handle_name_error(str(error))
        else:
            print("Encountered an unhandled error. Logged for review.")
    
    def handle_name_error(self, error_message):
        if "GPT4Agent" in error_message:
            print("Self-healing: Importing GPT4Agent dynamically.")
            try:
                GPT4Agent = importlib.import_module('gpt4_agent').GPT4Agent
                print("Successfully imported GPT4Agent.")
            except Exception as e:
                print(f"Failed to import GPT4Agent: {e}")
                logging.error(f"Failed self-healing for NameError: {e}")
        else:
            print(f"Could not resolve NameError: {error_message}")
            logging.error(f"Could not self-heal NameError: {error_message}")

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
        return "generic"

    def find_agent_for_task(self, task_keyword):
        for agent in self.agent_registry:
            if task_keyword in agent.role.lower():
                return agent
        return None
