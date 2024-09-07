class TaskManagerAgent:
    def __init__(self, agent_registry, agent_creator):
        """
        Task Manager Agent to assign tasks and recognize agent needs.
        """
        self.agent_registry = agent_registry  # Registry of available agents
        self.agent_creator = agent_creator    # Agent responsible for creating new agents

    def assign_task(self, task_description):
        # Analyze the task and assign it to the correct agent
        task_keywords = self.analyze_task(task_description)

        assigned_agent = self.find_agent_for_task(task_keywords)
        
        if not assigned_agent:
            # If no agent is available, create a new one
            assigned_agent = self.agent_creator.create_agent(task_keywords)
            self.agent_registry.append(assigned_agent)
        
        # Assign the task to the agent
        result = assigned_agent.perform_task(task_description)
        return result

    def analyze_task(self, task_description):
        """
        Analyze task and extract keywords or intent.
        """
        # Simplified task analysis, could use NLP models here for more complexity
        if "debug" in task_description.lower():
            return "debug"
        if "journal" in task_description.lower():
            return "journal"
        return "generic"

    def find_agent_for_task(self, task_keyword):
        """
        Find an appropriate agent based on task_keyword.
        """
        for agent in self.agent_registry:
            if task_keyword in agent.role.lower():
                return agent
        return None
