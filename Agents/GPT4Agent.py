class GPT4Agent:
    def __init__(self, name, role, personality, task_function=None):
        self.name = name
        self.role = role
        self.personality = personality
        self.task_function = task_function
    
    def perform_task(self, input_data):
        if self.task_function:
            return self.task_function(input_data)
        return f"{self.name} does not have a specific task function assigned."
    
    def introduce(self):
        return f"My name is {self.name}. I am responsible for {self.role}. {self.personality}"

