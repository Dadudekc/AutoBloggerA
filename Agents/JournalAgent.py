import json
import logging
import os

# Set up logging for the TradingRobotPlug project
log_directory = r'C:\Auto_Blogger\Logs'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

log_file_path = os.path.join(log_directory, 'journal_agent_log.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Import GPT4Agent
from GPT4Agent import GPT4Agent

class JournalAgent(GPT4Agent):
    def __init__(self):
        super().__init__(
            name="JournalistJourney",
            role="Journal",
            personality="Reflective and detailed journal writer.",
            task_function=self.journal_task_function  # Assign the journal task function
        )

    def journal_task_function(self, input_data):
        """
        Processes a journal entry task based on input JSON.
        """
        try:
            # Parse input_data as JSON
            json_data = json.loads(input_data)
            log_content = []

            for item in json_data["content"]:
                if "heading" in item:
                    log_content.append(f"Heading: {item['heading']}")
                elif "paragraph" in item:
                    log_content.append(f"Paragraph: {item['paragraph']}")
                elif "unordered_list" in item:
                    log_content.append(f"List: {', '.join(item['unordered_list'])}")
            
            logging.info(f"Journal entry processed: {log_content}")
            return f"Journal entry created with content: {log_content}"
        
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse input data as JSON: {e}")
            return f"Error: Failed to parse input data as JSON: {e}"

        except Exception as e:
            logging.error(f"An error occurred while processing journal task: {e}")
            return f"Error while processing journal task: {e}"

# Example Usage: Writing a report based on the TradingRobotPlug project

def main():
    """
    Example usage of JournalAgent for writing a report about the TradingRobotPlug project.
    """
    agent = JournalAgent()

    # Example report about the TradingRobotPlug project
    report_data = json.dumps({
        "content": [
            {"heading": "TradingRobotPlug Overview"},
            {"paragraph": "The TradingRobotPlug project is designed to revolutionize fintech by streamlining the process of training and backtesting stock models."},
            {"paragraph": "The system enables users to dynamically train stock models with multiple indicators, apply them to historical data for backtesting, and automate model deployment when performance meets the criteria."},
            {"unordered_list": [
                "Automated stock data fetching from Alpaca API.",
                "Support for multiple indicators including trend, momentum, and volatility.",
                "Real-time trade execution integration.",
                "Dynamic model training and backtesting framework."
            ]},
            {"paragraph": "The project incorporates advanced machine learning techniques and allows for scalable deployment across different stock tickers."},
            {"paragraph": "As part of the project’s evolution, advanced error-handling mechanisms and a self-healing infrastructure have been integrated into the system to improve resilience."}
        ]
    })

    # Agent processes the report data
    result = agent.perform_task(report_data)
    print(result)

if __name__ == "__main__":
    main()
