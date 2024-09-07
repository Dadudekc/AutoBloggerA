# -------------------------------------------------------------------
# File Path: Scripts/wordpress_publisher.py
# Description: Publishes journal entries to WordPress via the REST API.
# Supports draft mode and scheduling posts for future publication.
# -------------------------------------------------------------------

import requests
import base64
import logging
import datetime

# -------------------------------------------------------------------
# Section 1: Configuration Setup
# -------------------------------------------------------------------
# WordPress credentials (Replace with your credentials)
WORDPRESS_USERNAME = "DadudeKC"
WORDPRESS_PASSWORD = "your_password"
WORDPRESS_API_URL = "https://tradingrobotplug.com/wp-json/wp/v2/posts"

# -------------------------------------------------------------------
# Section 2: WordPress Publishing Function (Draft & Scheduled Publishing)
# -------------------------------------------------------------------
def publish_to_wordpress(title, content, publish_in_days=3):
    """
    Publishes the generated journal entry to a WordPress site as a draft and schedules it for future publication.
    
    Args:
        title (str): The title of the WordPress post.
        content (str): The content of the WordPress post in HTML format.
        publish_in_days (int): Number of days to delay the scheduled post (default is 3 days).

    Returns:
        bool: True if published successfully, False otherwise.
    """
    try:
        # Calculate the scheduled date (3 days from today, adjustable)
        scheduled_date = datetime.datetime.utcnow() + datetime.timedelta(days=publish_in_days)
        date_gmt = scheduled_date.isoformat() + "Z"  # Convert to WordPress GMT format

        # Logging scheduled date
        logging.info(f"Scheduled post for {scheduled_date}")

        # Encoding WordPress credentials for Basic Authentication
        auth = base64.b64encode(f"{WORDPRESS_USERNAME}:{WORDPRESS_PASSWORD}".encode()).decode()
        headers = {
            'Authorization': f'Basic {auth}',
            'Content-Type': 'application/json'
        }
        
        # WordPress post data
        data = {
            'title': title,
            'content': content,
            'status': 'draft',  # Save post as draft initially
            'date_gmt': date_gmt  # Schedule the post to be published at this date/time
        }
        
        # Sending POST request to WordPress API
        response = requests.post(WORDPRESS_API_URL, headers=headers, json=data)
        
        # Check if the post was successfully created
        if response.status_code == 201:
            logging.info(f'Post "{title}" saved as draft and scheduled for {scheduled_date}.')
            print(f'Post "{title}" saved as draft and scheduled for {scheduled_date}.')
            return True
        else:
            logging.error(f'Failed to publish post: {response.status_code}, Error: {response.text}')
            print(f'Failed to publish post: {response.status_code}, Error: {response.text}')
            return False

    except Exception as e:
        logging.error(f"Error publishing to WordPress: {e}")
        print(f"Error publishing to WordPress: {e}")
        return False

# -------------------------------------------------------------------
# Section 3: Example Usage (Main Section)
# -------------------------------------------------------------------
if __name__ == "__main__":
    # Example title and content
    journal_title = "Generated Project Journal Entry - Automated"
    journal_content = """
    <p>This is an example of an auto-generated project journal entry.</p>
    <p>It contains information about tasks completed, challenges faced, and next steps.</p>
    """

    # Publish the journal entry as a draft and schedule for 3 days later
    published_successfully = publish_to_wordpress(journal_title, journal_content, publish_in_days=3)
    
    if published_successfully:
        print("Journal entry published successfully.")
    else:
        print("Failed to publish journal entry.")
