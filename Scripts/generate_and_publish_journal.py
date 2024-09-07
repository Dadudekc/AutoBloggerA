# -------------------------------------------------------------------
# File Path: C:\Auto_Blogger\Scripts\generate_and_publish_journal.py
# Description: Main script to run the automation pipeline for generating
# and publishing journal entries. It fetches git commits, logs, schedules
# the journal generation, and publishes the journal entry to WordPress.
# -------------------------------------------------------------------

import os
import configparser
from git_commits_fetcher import fetch_git_commits
from journal_generator import generate_journal_entry
from logger import setup_logging
from notifier import send_email_notification
from schedule_manager import schedule_journal_posting

# -------------------------------------------------------------------
# Section 1: Load Configuration
# -------------------------------------------------------------------
config = configparser.ConfigParser()

# Construct the path to config.ini dynamically
config_file_path = os.path.join(os.path.dirname(__file__), 'config', 'config.ini')

# Check if the config file exists
if os.path.exists(config_file_path):
    config.read(config_file_path)
    print("Config file loaded successfully.")
else:
    raise FileNotFoundError(f"Config file not found at {config_file_path}")

# Fetch WordPress credentials and API URL from the config file
WORDPRESS_USERNAME = config.get('wordpress', 'username')
WORDPRESS_PASSWORD = config.get('wordpress', 'password')
WORDPRESS_API_URL = config.get('wordpress', 'api_url')

# Fetch OpenAI API key if needed (can be used elsewhere in the project)
OPENAI_API_KEY = config.get('openai', 'api_key')

# -------------------------------------------------------------------
# Section 2: Main Pipeline Function
# -------------------------------------------------------------------
# -------------------------------------------------------------------
# Section 2: Main Pipeline Function
# -------------------------------------------------------------------
def generate_and_publish_journal():
    try:
        # Comment out the Git logic
        """
        # Fetch Git commit history and activity as journal data
        print("Fetching git commits for journal data...")
        raw_data = fetch_git_commits()
        """

        # For now, provide dummy data in place of Git commits
        raw_data = "Sample journal data in place of git commits."

        # Generate the journal entry based on commits and project data
        print("Generating the journal entry...")
        journal_entry = generate_journal_entry(raw_data)

        # Log the generated journal entry
        setup_logging("Generated journal entry", journal_entry)

        # Schedule the journal entry to be posted at a later time
        print("Scheduling the journal entry for publishing...")
        schedule_journal_posting(journal_entry, WORDPRESS_USERNAME, WORDPRESS_PASSWORD, WORDPRESS_API_URL)
        """
        # Send a notification that the journal has been generated and scheduled
        send_email_notification("Journal generated and scheduled for publishing", "The journal entry was successfully generated and scheduled.")
        print("Journal entry successfully generated and scheduled for publishing.")
        """
        
    except Exception as e:
        setup_logging("Error during journal generation", str(e))
        send_email_notification(f"Journal generation failed: {str(e)}", "Please check the logs for more details.")
        print("An error occurred while generating the journal entry.")

# -------------------------------------------------------------------
# Example Usage (Main Section)
# -------------------------------------------------------------------
if __name__ == "__main__":
    generate_and_publish_journal()
