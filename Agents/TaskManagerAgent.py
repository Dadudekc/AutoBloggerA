class TaskManagerAgent:
    def __init__(self, agent_registry, agent_creator):
        self.agent_registry = agent_registry
        self.agent_creator = agent_creator
        self.log_file = "/Auto_Blogger/Logs/agent_dialogue_log.txt"
    
    def assign_task(self, task_description):
        task_keywords = self.analyze_task(task_description)
        assigned_agent = self.find_agent_for_task(task_keywords)
        
        if not assigned_agent:
            assigned_agent = self.agent_creator.create_agent(task_keywords)
            self.agent_registry.append(assigned_agent)
        
        # Assign the task and get the result
        result = assigned_agent.perform_task(task_description)
        
        # Log the conversation
        self.log_dialogue(assigned_agent.name, task_description, result)
        
        return result

    def log_dialogue(self, agent_name, task_description, result):
        """
        Logs the dialogue between agents and their tasks.
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"{timestamp} - {agent_name} handled task '{task_description}' with result: {result}\n"
        
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
