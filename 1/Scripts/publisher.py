# -------------------------------------------------------------------
# File Path: scripts/publisher.py
# Description: Publishes generated journal entries via API (e.g., WordPress REST API).
# -------------------------------------------------------------------

import requests

# -------------------------------------------------------------------
# Section 1: Function to publish journal entry
# -------------------------------------------------------------------
def publish_journal_to_wordpress(title, content):
    url = 'https://yourwordpresssite.com/wp-json/wp/v2/posts'
    headers = {
        'Authorization': 'Bearer YOUR_API_TOKEN'
    }
    data = {
        'title': title,
        'content': content,
        'status': 'publish'
    }
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        print('Post published successfully!')
    else:
        print(f'Failed to publish post: {response.status_code}')

# -------------------------------------------------------------------
# Example Usage (Main Section)
# -------------------------------------------------------------------
if __name__ == "__main__":
    # Load the HTML from a file (or the rendered content from template_renderer.py)
    with open("journal_entry_july_3_2024.html", "r") as f:
        html_content = f.read()
    
    publish_journal_to_wordpress("Journal Entry - July 3, 2024", html_content)
