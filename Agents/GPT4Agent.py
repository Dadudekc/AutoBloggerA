class GPT4Agent:
    def __init__(self, name, role, personality, task_function):
        """
        Initialize the GPT4Agent with a name, role, personality, and task function.
        
        :param name: The name of the agent (e.g., "Debugger", "Journalist").
        :param role: The role of the agent (e.g., "Debugging", "Data Fetching").
        :param personality: A description of the agent's personality.
        :param task_function: The function the agent will use to perform its task.
        """
        self.name = name
        self.role = role
        self.personality = personality
        self.task_function = task_function

    def perform_task(self, input_data):
        """
        Execute the task function with the provided input data.
        
        :param input_data: The input data required for the task (e.g., an error traceback, journal content, API parameters).
        :return: The result of the task function.
        """
        return self.task_function(input_data)

    def introduce(self):
        """
        Introduce the agent by returning its name, role, and personality.
        
        :return: A string introducing the agent.
        """
        return f"My name is {self.name}. I am responsible for {self.role}. {self.personality}"

