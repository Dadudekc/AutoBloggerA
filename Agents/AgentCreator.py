import json
import subprocess  # For running linting and static analysis tools like pylint, flake8

class AgentCreator:
    def __init__(self, json_config_file):
        """
        Initialize the AgentCreator with agent configurations loaded from a JSON file.
        """
        with open(json_config_file, 'r') as file:
            self.config = json.load(file)

    def create_agent(self, task_keyword):
        """
        Dynamically creates a new agent based on the task keyword using JSON configuration.
        """
        for agent_data in self.config['agents']:
            if agent_data['task_keyword'] == task_keyword:
                return GPT4Agent(
                    name=agent_data['name'],
                    role=agent_data['role'],
                    personality=agent_data['personality'],
                    task_function=getattr(self, agent_data['task_function'])
                )
        return None  # No matching agent found

    def debug_task_function(self, error_traceback):
        """
        Task function for debugging agents.
        """
        return f"Analyzing and fixing the following error: {error_traceback}"

    def journal_task_function(self, input_data):
        """
        Task function for journal-writing agents.
        """
        return f"Writing a journal entry: {input_data}"

    def fetch_data_function(self, api_params):
        """
        Task function for fetching financial data.
        """
        return f"Fetching financial data with parameters: {api_params}"

    def strategy_task_function(self, strategy_params):
        """
        Task function for trading strategy agents.
        """
        return f"Generating trading signals based on strategy: {strategy_params}"

    def review_code_function(self, project_path):
        """
        Task function for the CodeReviewer agent. It reviews the codebase to find errors using static analysis tools.
        :param project_path: Path to the project directory to review
        :return: A summary of code issues found
        """
        # Example using pylint to check Python code for errors
        try:
            print(f"Reviewing code in: {project_path}")
            result = subprocess.run(["pylint", project_path], capture_output=True, text=True)
            return result.stdout
        except Exception as e:
            return f"Error while reviewing code: {e}"

