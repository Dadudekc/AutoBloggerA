import openai
import logging
import configparser
import os

# Set up logging
logging.basicConfig(level=logging.INFO)

# Define the path to your config file
config_file_path = os.path.join(os.path.dirname(__file__), 'config/config.ini')

# Check if the config file exists
if os.path.exists(config_file_path):
    config = configparser.ConfigParser()
    config.read(config_file_path)
    print("Config file loaded successfully.")
else:
    print(f"Config file not found at {config_file_path}")
    raise FileNotFoundError(f"Config file not found at {config_file_path}")

# Set up OpenAI API key
try:
    openai.api_key = config.get('openai', 'api_key')
except configparser.NoSectionError:
    logging.error("No 'openai' section found in config.ini.")
    raise
except configparser.NoOptionError:
    logging.error("No 'api_key' found in 'openai' section of config.ini.")
    raise

def generate_journal_entry(prompt):
    """
    Function to generate a journal entry using GPT-3.5-turbo or GPT-4.
    """
    try:
        # Use the correct ChatCompletion endpoint for chat models like gpt-3.5-turbo
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can also use "gpt-4" if you have access
            messages=[
                {"role": "system", "content": "You are an assistant that helps generate project journal entries."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        # Extract the generated content
        journal_entry = response['choices'][0]['message']['content']
        return journal_entry
    except Exception as e:
        logging.error(f"Error generating journal entry: {e}")
        return None

# Example usage
if __name__ == "__main__":
    prompt = "Generate a project journal entry based on the following accomplishments..."
    journal_entry = generate_journal_entry(prompt)
    
    if journal_entry:
        print("Generated Journal Entry:")
        print(journal_entry)
    else:
        print("Failed to generate journal entry.")
