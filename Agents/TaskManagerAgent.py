import logging

class TaskManagerAgent:
    def __init__(self, agent_registry, agent_creator):
        """
        Initialize the TaskManagerAgent with a list of agents and an agent creator.
        :param agent_registry: A list of registered agents that can handle tasks.
        :param agent_creator: The agent creator responsible for generating new agents.
        """
        self.agent_registry = agent_registry
        self.agent_creator = agent_creator
        logging.info("TaskManagerAgent initialized with registered agents.")

    def assign_task(self, task_description):
        """
        Assign a task to an appropriate agent based on the task description.
        :param task_description: A string describing the task to be performed.
        :return: The result of the task execution.
        """
        # Extract task keyword from the task description
        task_keywords = self.analyze_task(task_description)
        logging.info(f"Assigning task with keywords '{task_keywords}' based on description: {task_description}")
        
        # Try to find an existing agent that can handle the task
        assigned_agent = self.find_agent_for_task(task_keywords)
        
        if not assigned_agent:
            # No agent found, try to create a new agent dynamically
            logging.warning(f"No agent found for task '{task_keywords}', attempting to create a new agent.")
            assigned_agent = self.agent_creator.create_agent(task_keywords)
            if assigned_agent:
                self.agent_registry.append(assigned_agent)
                logging.info(f"New agent '{assigned_agent.name}' created for task '{task_keywords}'.")
            else:
                logging.error(f"Failed to create an agent for task: {task_keywords}")
                return f"Task '{task_keywords}' could not be handled."

        # Task is assigned to the found or created agent
        logging.info(f"Task assigned to agent: {assigned_agent.name}")
        result = assigned_agent.perform_task(task_description)
        logging.info(f"Task '{task_description}' completed by agent '{assigned_agent.name}' with result: {result}")
        return result

    def analyze_task(self, task_description):
        """
        Analyze the task description and extract a keyword that can be used to assign the task.
        :param task_description: A string containing the task description.
        :return: A task keyword to match against agents.
        """
        # Use simple keyword matching for now, but this can be expanded with NLP in the future
        keywords = {
            "finance": ["finance", "budget", "expense", "accounting"],
            "hr": ["hr", "recruit", "employee", "payroll"],
            "operations": ["operations", "logistics", "supply chain", "project"],
            "marketing": ["marketing", "campaign", "social media", "brand strategy"]
        }
        
        for keyword, synonyms in keywords.items():
            if any(word in task_description.lower() for word in synonyms):
                return keyword
        
        # Fallback to generic if no match is found
        logging.info(f"No specific keyword found in task description, defaulting to 'generic'.")
        return "generic"

    def find_agent_for_task(self, task_keyword):
        """
        Search the agent registry for an agent capable of handling the task based on the keyword.
        :param task_keyword: The keyword representing the task category (e.g., 'finance', 'hr').
        :return: The agent that can handle the task, or None if no agent is found.
        """
        for agent in self.agent_registry:
            if task_keyword in agent.role.lower():
                logging.info(f"Found agent '{agent.name}' for task keyword: {task_keyword}")
                return agent
        
        logging.warning(f"No agent found for task keyword: {task_keyword}")
        return None
