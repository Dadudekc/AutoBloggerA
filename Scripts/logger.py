# -------------------------------------------------------------------
# File Path: Scripts/logger.py
# Description: Sets up a standardized logging mechanism for the project.
# Supports logging to a file and console with different log levels.
# -------------------------------------------------------------------

import logging
import os

# -------------------------------------------------------------------
# Section 1: Log File Setup
# -------------------------------------------------------------------
# Directory where log files will be stored
LOG_DIR = "Logs"
LOG_FILE_NAME = "journal_automation.log"

# Create the log directory if it doesn't exist
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE_NAME)

# -------------------------------------------------------------------
# Section 2: Logging Configuration
# -------------------------------------------------------------------

def setup_logging(message, data=None):
    """
    Logs messages to a file or the console.

    Args:
        message (str): The message to log.
        data (str, optional): Additional data to log.
    """
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", filename="app.log", filemode="a")
    logging.info(message)
    
    if data:
        logging.info(data)


# -------------------------------------------------------------------
# Section 3: Example Usage (Main Section)
# -------------------------------------------------------------------
if __name__ == "__main__":
    # Initialize logging
    setup_logging("Test message", "Additional log data.")

    # Example log messages
    logging.info("This is an INFO level message.")
    logging.warning("This is a WARNING level message.")
    logging.error("This is an ERROR level message.")
