# -------------------------------------------------------------------
# File Path: C:/Auto_Blogger/Agents/AgentCreator.py
# Description: Handles the creation and management of various agents based on task keywords.
# This script is designed to work within the Auto_Blogger system, with
# standardized logging, error handling, and configuration management.
# -------------------------------------------------------------------

import os
import subprocess
import json
import logging
from GPT4Agent import GPT4Agent  # Ensure GPT4Agent is imported correctly

# -------------------------------------------------------------------
# Section 1: Logging Setup
# -------------------------------------------------------------------

# Ensure the log directory exists
log_directory = r'C:\Auto_Blogger\Logs'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Initialize logging and ensure it logs to the specified file
log_file_path = os.path.join(log_directory, 'agent_victor_errors.log')
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# -------------------------------------------------------------------
# Section 2: AgentCreator Class Definition
# -------------------------------------------------------------------

class AgentCreator:
    def __init__(self, json_config_file):
        """
        Initialize the AgentCreator with agent configurations loaded from a JSON file.
        """
        with open(json_config_file, 'r') as file:
            self.config = json.load(file)

    # -------------------------------------------------------------------
    # Section 3: Agent Creation Method
    # -------------------------------------------------------------------

    def create_agent(self, task_keyword):
        """
        Dynamically creates a new agent based on the task keyword using JSON configuration.
        :param task_keyword: The keyword representing the type of task the agent will handle.
        :return: An instance of GPT4Agent with the appropriate task function.
        """
        # Look for an agent configuration in the JSON that matches the task keyword
        for agent_data in self.config['agents']:
            if task_keyword in agent_data['task_keyword']:
                return GPT4Agent(
                    name=agent_data['name'],
                    role=agent_data['role'],
                    personality=agent_data['personality'],
                    task_function=getattr(self, agent_data['task_function'])
                )
        logging.error(f"No matching agent found for task keyword: {task_keyword}")
        return None  # No matching agent found

    # -------------------------------------------------------------------
    # Section 4: Task Functions for Agents
    # These functions define how specific tasks should be handled by agents.
    # -------------------------------------------------------------------

    def debug_task_function(self, error_traceback):
        """
        Task function for debugging agents.
        :param error_traceback: The traceback string representing the error that occurred.
        :return: A string representing the debugging result.
        """
        return f"Analyzing and fixing the following error: {error_traceback}"

    def journal_task_function(self, input_data):
        """
        Task function for journal-writing agents.
        :param input_data: The input data for the journal entry.
        :return: A string representing the journal entry result.
        """
        return f"Writing a journal entry: {input_data}"

    def fetch_data_function(self, api_params):
        """
        Task function for fetching financial data.
        :param api_params: Parameters needed to fetch data.
        :return: A string indicating the result of the data fetch.
        """
        return f"Fetching financial data with parameters: {api_params}"

    def strategy_task_function(self, strategy_params):
        """
        Task function for trading strategy agents.
        :param strategy_params: Parameters needed to generate trading signals.
        :return: A string representing the generated signals.
        """
        return f"Generating trading signals based on strategy: {strategy_params}"

    # -------------------------------------------------------------------
    # Section 5: Specialized Task Functions
    # These functions simulate handling specific tasks like finance, HR, etc.
    # -------------------------------------------------------------------

    def finance_management_function(self, task_data):
        """
        Simulates handling of finance tasks, such as budget tracking, expense reports, etc.
        :param task_data: Data related to the financial task.
        :return: A string representing the result of the finance task.
        """
        if "budget" in task_data.lower():
            logging.info("Processing budget report...")
            return f"FinanceManager: Processing budget report for {task_data}"
        elif "expense" in task_data.lower():
            logging.info("Handling expense reports...")
            return f"FinanceManager: Handling expense reports for {task_data}"
        else:
            logging.info("Handling general financial task.")
            return f"FinanceManager: Handling financial task: {task_data}"

    def hr_management_function(self, task_data):
        """
        Simulates handling HR tasks like recruitment, employee management, and payroll.
        :param task_data: Data related to the HR task.
        :return: A string representing the result of the HR task.
        """
        if "recruit" in task_data.lower():
            logging.info("Recruiting new employees...")
            return f"HRManager: Recruiting employees for {task_data}"
        elif "payroll" in task_data.lower():
            logging.info("Processing payroll...")
            return f"HRManager: Processing payroll for {task_data}"
        elif "employee relations" in task_data.lower():
            logging.info("Managing employee relations...")
            return f"HRManager: Managing employee relations for {task_data}"
        else:
            logging.info("Handling general HR task.")
            return f"HRManager: Handling HR task: {task_data}"

    def operations_management_function(self, task_data):
        """
        Simulates handling operations tasks such as logistics, supply chain management, or project coordination.
        :param task_data: Data related to the operations task.
        :return: A string representing the result of the operations task.
        """
        if "logistics" in task_data.lower():
            logging.info("Overseeing logistics operations...")
            return f"OperationsManager: Overseeing logistics for {task_data}"
        elif "supply chain" in task_data.lower():
            logging.info("Managing supply chain...")
            return f"OperationsManager: Managing supply chain for {task_data}"
        elif "project coordination" in task_data.lower():
            logging.info("Coordinating projects...")
            return f"OperationsManager: Coordinating project: {task_data}"
        else:
            logging.info("Handling general operations task.")
            return f"OperationsManager: Handling operations task: {task_data}"

    def marketing_management_function(self, task_data):
        """
        Simulates handling marketing tasks like launching campaigns, handling social media, or managing brand strategy.
        :param task_data: Data related to the marketing task.
        :return: A string representing the result of the marketing task.
        """
        if "campaign" in task_data.lower():
            logging.info("Launching marketing campaign...")
            return f"MarketingManager: Launching campaign for {task_data}"
        elif "social media" in task_data.lower():
            logging.info("Managing social media accounts...")
            return f"MarketingManager: Managing social media for {task_data}"
        elif "brand strategy" in task_data.lower():
            logging.info("Developing brand strategy...")
            return f"MarketingManager: Developing brand strategy for {task_data}"
        else:
            logging.info("Handling general marketing task.")
            return f"MarketingManager: Handling marketing task: {task_data}"

    # -------------------------------------------------------------------
    # Section 6: Code Review Function
    # -------------------------------------------------------------------

    def review_code_function(self, project_path):
        """
        Task function for the CodeReviewer agent. It reviews the codebase to find errors using static analysis tools.
        :param project_path: Path to the project directory to review.
        :return: A summary of code issues found using pylint.
        """
        try:
            logging.info(f"Reviewing code in: {project_path}")
            result = subprocess.run(["pylint", project_path], capture_output=True, text=True)
            return result.stdout
        except Exception as e:
            logging.error(f"Error while reviewing code: {e}")
            return f"Error while reviewing code: {e}"
