class TaskManagerAgent:
    def __init__(self, agent_registry, agent_creator):
        self.agent_registry = agent_registry
        self.agent_creator = agent_creator
        self.victor = AgentVictor()  # Initialize AgentVictor
        self.victor.agent_registry = self.agent_registry
        self.victor.agent_creator = self.agent_creator
    
    def assign_task(self, task_description):
        """
        TaskManager simply passes tasks to AgentVictor, who decides how to handle them.
        """
        result = self.victor.handle_task(task_description)
        return result
