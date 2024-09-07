# -------------------------------------------------------------------
# File Path: Scripts/git_commits_fetcher.py
# Description: Fetches Git commit history for a specific number of days or
# commit count and formats it for use in project journal entries.
# -------------------------------------------------------------------

import subprocess
import logging

# -------------------------------------------------------------------
# Section 1: Fetch Git Commit Messages
# -------------------------------------------------------------------
def fetch_git_commits(days_back=3, limit=None):
    """
    Fetches Git commit messages from the past specified number of days or commits.
    
    Args:
        days_back (int): Number of days back to fetch commits (default is 3 days).
        limit (int): Optional limit on the number of commits to fetch (default is None).
        
    Returns:
        str: A formatted string of the commit messages.
    """
    try:
        # Command to fetch Git logs from the last few days
        git_command = f'git log --since="{days_back}.days" --pretty=format:"%h - %s (%ci)"'

        if limit:
            git_command += f" -n {limit}"

        # Execute the command and capture the output
        logging.info(f"Executing Git command: {git_command}")
        commit_logs = subprocess.check_output(git_command, shell=True).decode('utf-8').strip()

        if not commit_logs:
            logging.info("No recent commits found.")
            return "No recent commits found."
        
        # Format the commit logs for journal entry
        formatted_commits = f"Recent Commits (Last {days_back} days):\n{commit_logs}"
        logging.info(f"Fetched and formatted Git commits:\n{formatted_commits}")
        return formatted_commits
    
    except subprocess.CalledProcessError as e:
        logging.error(f"Error fetching Git commits: {e}")
        return "Error retrieving Git commits."

# -------------------------------------------------------------------
# Section 2: Example Usage (Main Section)
# -------------------------------------------------------------------
if __name__ == "__main__":
    # Fetch commits from the last 3 days, limit to the 5 most recent commits
    git_commits = fetch_git_commits(days_back=3, limit=5)
    
    if git_commits:
        print(f"Git Commits Fetched:\n{git_commits}")
    else:
        print("No Git commits found or error fetching commits.")

