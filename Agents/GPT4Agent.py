import logging
import os

# Set up logging for the TradingRobotPlug project
log_directory = r'C:\Auto_Blogger\Logs'
log_file_path = os.path.join(log_directory, 'gpt4_agent_log.log')

if not os.path.exists(log_directory):
    os.makedirs(log_directory)

logging.basicConfig(filename=log_file_path, level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')


class GPT4Agent:
    def __init__(self, name, role, personality, task_function=None):
        """
        Initialize the GPT4Agent with a name, role, personality, and an optional task function.
        :param name: The name of the agent.
        :param role: The role of the agent within the TradingRobotPlug system.
        :param personality: The personality traits of the agent.
        :param task_function: The task function the agent performs (optional).
        """
        self.name = name
        self.role = role
        self.personality = personality
        self.task_function = task_function

        logging.info(f"Initialized agent '{self.name}' with role '{self.role}'.")

    def perform_task(self, input_data):
        """
        Perform the agent's task using the provided input data.
        :param input_data: Data required for the task.
        :return: Result of the task execution or a message if no task function is assigned.
        """
        if self.task_function:
            logging.info(f"Agent '{self.name}' performing task with input: {input_data}")
            return self.task_function(input_data)
        logging.warning(f"Agent '{self.name}' does not have a specific task function assigned.")
        return f"{self.name} does not have a specific task function assigned."

    def introduce(self):
        """
        Introduce the agent by returning its name, role, and personality.
        :return: Introduction string.
        """
        intro = f"My name is {self.name}. I am responsible for {self.role}. {self.personality}"
        logging.info(f"Agent '{self.name}' introduction: {intro}")
        return intro


# Example Usage: OrchestratorOverseer performing a general task

def main():
    """
    Example usage of OrchestratorOverseer, the central agent of the AI company responsible for overseeing tasks.
    """
    # Create the OrchestratorOverseer agent
    overseer = GPT4Agent(
        name="OrchestratorOverseer",
        role="System Orchestrator",
        personality="Strategic and authoritative, overseeing all agents in the AI company and ensuring tasks are properly assigned and executed."
    )

    # Agent introduces itself
    print(overseer.introduce())

    # Example of performing a task
    task_data = "Oversee and coordinate system tasks for TradingRobotPlug"
    result = overseer.perform_task(task_data)
    print(result)


if __name__ == "__main__":
    main()
