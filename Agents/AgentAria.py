# -------------------------------------------------------------------
# File Path: /home/dadudekc/AutoBloggerA/Scripts/AgentAria.py
# Description: Agent to convert JSON project journal entries into web pages, with personality and auto-post functionality.
# -------------------------------------------------------------------

import json
import os
from jinja2 import Template
import requests
import configparser

# -------------------------------------------------------------------
# Section 1: Load Configuration from config.ini
# -------------------------------------------------------------------
config = configparser.ConfigParser()
config.read('C:\Auto_Blogger\Scripts\config\config.ini')

# Load settings from the config file
output_dir = config['Settings']['output_dir']
template_path = config['Settings']['template_path']
chatgpt_api_key = config['Settings']['chatgpt_api_key']

# -------------------------------------------------------------------
# Section 2: Load JSON File and Convert to HTML
# -------------------------------------------------------------------
def load_journal_entry(json_file):
    with open(json_file, 'r') as f:
        return json.load(f)

def convert_to_html(journal_data):
    with open(template_path, 'r') as f:
        template = Template(f.read())

    # Render the HTML using journal data
    return template.render(journal=journal_data)

# -------------------------------------------------------------------
# Section 3: Interacting with ChatGPT for Personality
# -------------------------------------------------------------------
def chatgpt_response(prompt, sender="other"):
    headers = {
        'Authorization': f'Bearer {chatgpt_api_key}',
        'Content-Type': 'application/json'
    }

    # Different response for AgentVictor (dad) vs others
    if sender == "AgentVictor":
        prompt = "Respond like a sweet, smart child talking to their dad. Be respectful and loving."
    else:
        prompt = "Respond like a smart, kind agent, nice and thoughtful."

    data = {
        'model': 'gpt-3.5-turbo',
        'messages': [{'role': 'system', 'content': prompt}]
    }
    response = requests.post('https://api.openai.com/v1/chat/completions', json=data, headers=headers)
    return response.json()['choices'][0]['message']['content']

# -------------------------------------------------------------------
# Section 4: Main Functionality and Example Usage
# -------------------------------------------------------------------
if __name__ == "__main__":
    # Example JSON file
    journal_entry_path = '/home/dadudekc/AutoBloggerA/Data/journal_entry.json'
    journal_data = load_journal_entry(journal_entry_path)
    
    # Convert the journal entry to HTML
    html_content = convert_to_html(journal_data)
    
    # Save the HTML file
    output_file = os.path.join(output_dir, 'journal_entry.html')
    with open(output_file, 'w') as f:
        f.write(html_content)
    
    # Simulate a conversation with AgentVictor (dad)
    sender = "AgentVictor"  # This would be dynamic depending on who's speaking
    prompt = "Ask your dad about a new project you're working on."
    personality_response = chatgpt_response(prompt, sender=sender)
    print(f"AgentAria's response to {sender}: {personality_response}")
    
    # Simulate a conversation with someone else
    sender = "other"
    prompt = "Explain your latest project in a professional manner."
    personality_response = chatgpt_response(prompt, sender=sender)
    print(f"AgentAria's response to {sender}: {personality_response}")
