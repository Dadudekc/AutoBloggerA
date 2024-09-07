# -------------------------------------------------------------------
# File Path: generate_and_publish_journal.py
# Description: Automates the generation of project journal entries using GPT-4, 
# pulls accomplishments from Git, and schedules WordPress posts for future publication.
# -------------------------------------------------------------------

import openai
import requests
import base64
import subprocess
import datetime

# -------------------------------------------------------------------
# Section 1: Configuration Setup
# -------------------------------------------------------------------
# Set up OpenAI API Key (Replace with your API key)
OPENAI_API_KEY = "sk-S7p0EcbK1aql56yU9TGfjuUXOHRZct4ejb3jowvKTDT3BlbkFJSjgjU2lC4vqvdaFnbChxn-gVRLFlPdSbU9juKMHCQA"
openai.api_key = OPENAI_API_KEY

# WordPress credentials (Replace with your WordPress username and application password)
WORDPRESS_USERNAME = "your_username"
WORDPRESS_PASSWORD = "your_password"
WORDPRESS_API_URL = "https://tradingrobotplug.com/wp-json/wp/v2/posts"

# Number of days back to fetch Git commits (modify as needed)
DAYS_BACK = 3

# -------------------------------------------------------------------
# Section 2: Fetch Git Commits for Accomplishments
# -------------------------------------------------------------------
def fetch_git_commits(days_back=DAYS_BACK):
    """
    Fetches Git commit messages from the last `days_back` days.
    
    Args:
        days_back (int): Number of days back to fetch commits.
    
    Returns:
        str: A formatted string with the latest commit messages.
    """
    try:
        # Fetch commit messages from the past few days
        command = f'git log --since="{days_back}.days" --pretty=format:"%s"'
        commit_messages = subprocess.check_output(command, shell=True).decode('utf-8')
        
        if not commit_messages:
            return "No recent commits found."
        
        return f"Recent Commits:\n{commit_messages.strip()}"
    except Exception as e:
        print(f"Error fetching Git commits: {e}")
        return "Error retrieving Git commits."

# -------------------------------------------------------------------
# Section 3: Journal Entry Generation using GPT-4
# -------------------------------------------------------------------
def generate_journal_entry(prompt_template):
    """
    Generates a project journal entry using GPT-4 based on the provided prompt template.
    
    Args:
        prompt_template (str): The template prompt for GPT-4.

    Returns:
        str: Generated journal entry as text.
    """
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt_template,
            max_tokens=1024,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error generating journal entry: {e}")
        return None

# -------------------------------------------------------------------
# Section 4: WordPress Publishing Function (Draft and Scheduled)
# -------------------------------------------------------------------
def publish_to_wordpress(title, content, publish_in_days=3):
    """
    Publishes the generated journal entry to a WordPress site as a draft and schedules it for future publication.
    
    Args:
        title (str): The title of the WordPress post.
        content (str): The content of the WordPress post in HTML format.
        publish_in_days (int): Number of days to delay the scheduled post.

    Returns:
        None
    """
    try:
        # Calculate the scheduled date (3 days from today)
        scheduled_date = datetime.datetime.utcnow() + datetime.timedelta(days=publish_in_days)
        date_gmt = scheduled_date.isoformat() + "Z"  # Convert to WordPress GMT format

        # Encoding WordPress credentials for Basic Authentication
        auth = base64.b64encode(f"{WORDPRESS_USERNAME}:{WORDPRESS_PASSWORD}".encode()).decode()
        headers = {
            'Authorization': f'Basic {auth}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'title': title,
            'content': content,
            'status': 'draft',  # Initially save as draft
            'date_gmt': date_gmt  # Schedule the post to be published 3 days later
        }
        
        response = requests.post(WORDPRESS_API_URL, headers=headers, json=data)
        
        if response.status_code == 201:
            print(f'Post "{title}" saved as draft and scheduled for {scheduled_date}!')
        else:
            print(f'Failed to publish post: {response.status_code}, Error: {response.text}')
    except Exception as e:
        print(f"Error publishing to WordPress: {e}")

# -------------------------------------------------------------------
# Section 5: Prompt Template Definition
# -------------------------------------------------------------------
def get_journal_prompt(git_accomplishments):
    """
    Returns a standardized prompt template for generating journal entries, including recent Git accomplishments.

    Args:
        git_accomplishments (str): Recent Git commits to include in the prompt.

    Returns:
        str: A prompt template string for GPT-4.
    """
    return f"""
    Use this conversation to make a project journal entry following the standards and guides of the template below. 
    Base the title of the entry off of the conversation.

    ## Work Completed
    Provide a detailed and structured account of the tasks you accomplished. Address the following points:
    - **Objectives and Goals:** Clearly state the main objectives and goals for the work session.
    - **Actions Taken:** Describe key actions taken and steps completed, providing context for each.
    - **Challenges and Breakthroughs:** Discuss any major breakthroughs or challenges encountered and how they were resolved.
    - **Results and Impact:** Summarize the outcomes of your efforts and how they contribute to the project's progress. Highlight the impact on the overall project.

    {git_accomplishments}

    ## Skills and Technologies Used
    Detail the skills and technologies you utilized. Highlight any new skills acquired or existing skills that were particularly useful.

    ## Lessons Learned
    Reflect on the key takeaways from the session. Address unexpected challenges and future application.

    ## To-Do
    Outline the next steps and tasks that need to be completed.
    """

# -------------------------------------------------------------------
# Example Usage (Main Section)
# -------------------------------------------------------------------
if __name__ == "__main__":
    # Fetch recent Git commit messages to include in the journal entry
    git_accomplishments = fetch_git_commits()

    # Define the journal prompt using the template and Git commits
    journal_prompt = get_journal_prompt(git_accomplishments)

    # Generate the journal entry
    generated_journal_entry = generate_journal_entry(journal_prompt)
    
    if generated_journal_entry:
        print(f"Generated Journal Entry:\n{generated_journal_entry}")

        # Define the title for the WordPress post
        journal_title = "Generated Project Journal Entry - Automated"

        # Publish the generated journal entry to WordPress (scheduled 3 days later)
        publish_to_wordpress(journal_title, f"<p>{generated_journal_entry}</p>", publish_in_days=3)
    else:
        print("Failed to generate journal entry.")
