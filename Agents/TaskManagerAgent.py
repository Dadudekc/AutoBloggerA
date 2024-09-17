import logging

class TaskManagerAgent:
    def __init__(self, agent_registry, agent_creator):
        self.agent_registry = agent_registry
        self.agent_creator = agent_creator
        logging.info("TaskManagerAgent initialized with registered agents.")

    def assign_task(self, task_description):
        """
        Assign a task to an appropriate agent based on the task description.
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
        """
        # Add more detailed keyword matching for common tasks
        if "debug" in task_description.lower():
            return "debug"
        if "journal" in task_description.lower():
            return "journal"
        if "strategy" in task_description.lower():
            return "strategy"
        if "finance" in task_description.lower():
            return "finance"
        if "hr" in task_description.lower() or "recruit" in task_description.lower():
            return "hr"  # Map HR-related tasks
        if "operations" in task_description.lower():
            return "operations"
        if "marketing" in task_description.lower():
            return "marketing"
        return "generic"  # Catch-all for tasks that don't match

        
        # Default to generic if no specific match
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
