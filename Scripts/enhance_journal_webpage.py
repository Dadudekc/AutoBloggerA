# -------------------------------------------------------------------
# File Path: Scripts/enhance_journal_webpage.py
# Description: Enhances the generated journal webpage by adding relevant images,
# modifying fonts to match dadudekc.com, and adjusting the background with 42% opacity.
# -------------------------------------------------------------------

import os
import openai
import requests
import configparser
import time
import json
from bs4 import BeautifulSoup
import shutil

# Paths to the generated HTML and other necessary resources
journal_html_path = os.path.join(os.getcwd(), "project_journal_entry.html")

# Load the config.ini file
config_file_path = os.path.join(os.path.dirname(__file__), 'config/config.ini')
config = configparser.ConfigParser()

if os.path.exists(config_file_path):
    config.read(config_file_path)
    print("Config file loaded successfully.")
else:
    raise FileNotFoundError(f"Config file not found at {config_file_path}")

# Fetch OpenAI credentials from config file
openai.api_key = config.get('openai', 'api_key')

# Directory where images will be stored
images_folder = os.path.join(os.getcwd(), "images")

# Ensure the images folder exists
if not os.path.exists(images_folder):
    os.makedirs(images_folder)

# Step 1: Modify the generated HTML for better readability
def modify_journal_html_for_readability(html_content):
    """
    Modify the HTML content to improve text readability by adjusting background opacity to 42%
    and changing the text color to white.
    """
    try:
        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Modify the CSS in the <style> section
        for style_tag in soup.find_all('style'):
            if "body" in style_tag.string:
                style_tag.string = style_tag.string.replace(
                    "opacity: 0.4;", "opacity: 0.42;"  # Update background opacity
                ).replace(
                    "color: black;", "color: white;"  # Change text color to white
                )

        # Modify the section background to enhance readability
        for section in soup.find_all("div", class_="section"):
            section["style"] = "background-color: rgba(0, 0, 0, 0.7); padding: 20px; border-radius: 15px;"

        return str(soup)

    except Exception as e:
        print(f"Error modifying the HTML content: {e}")
        return html_content

# Function to fetch HTML file content
def fetch_html_file(html_file_path):
    """
    Fetches the content of the HTML file for further processing.
    """
    try:
        with open(html_file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error fetching HTML file: {e}")
        return None

# Step 2: Modify the HTML to include relevant images
def add_relevant_images(html_content, prompt):
    """
    Generate and add relevant images of people related to the topic.
    """
    try:
        # Create an image with DALL·E based on the topic
        response = openai.Image.create(prompt=prompt, n=1, size="1024x1024")
        image_url = response['data'][0]['url']

        # Download the image and save it locally
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        image_filename = f"relevant_image_{timestamp}.png"
        image_path = os.path.join(images_folder, image_filename)
        image_data = requests.get(image_url).content
        with open(image_path, 'wb') as handler:
            handler.write(image_data)

        # Add the image to the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        img_tag = soup.new_tag("img", src=f"images/{image_filename}", alt="Relevant image", style="max-width: 100%; height: auto; display: block; margin: 20px auto;")
        soup.body.insert(0, img_tag)  # Insert image at the top

        return str(soup)

    except Exception as e:
        print(f"Error generating or adding image: {e}")
        return html_content

# Step 3: Add the dadudekc.com font styles to the HTML
def add_custom_fonts(html_content):
    """
    Adds custom fonts matching those used on dadudekc.com.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Assuming the fonts used on dadudekc.com are Google Fonts
    font_link = soup.new_tag("link", href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap", rel="stylesheet")
    soup.head.append(font_link)

    # Update the body font family
    style_tag = soup.new_tag("style")
    style_tag.string = """
    body {
        font-family: 'Montserrat', sans-serif;
    }
    """
    soup.head.append(style_tag)

    return str(soup)

# Step 4: Add a new background image

def update_background_image(html_content):
    """
    Replaces the background image with a new one fitting the journal's theme,
    ensuring it covers the entire page and is fixed like on dadudekc.com.
    """
    background_prompt = "Create a clean, minimal, professional background image with a dark muted tone that matches the theme of project progress."
    try:
        # Generate a new background image using DALL·E
        response = openai.Image.create(prompt=background_prompt, n=1, size="1024x1024")
        image_url = response['data'][0]['url']

        # Download the image
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        image_filename = f"background_{timestamp}.png"
        image_path = os.path.join(images_folder, image_filename)
        image_data = requests.get(image_url).content
        with open(image_path, 'wb') as handler:
            handler.write(image_data)

        # Update the background in the HTML to be fixed and cover the entire page
        soup = BeautifulSoup(html_content, 'html.parser')
        for style_tag in soup.find_all('style'):
            if "background" in style_tag.string:
                style_tag.string = style_tag.string.replace(
                    "background:", 
                    f"background: url('images/{image_filename}') no-repeat center center fixed; background-attachment: fixed; background-size: cover; opacity: 0.42;"
                )
        
        return str(soup)

    except Exception as e:
        print(f"Error generating or adding background image: {e}")
        return html_content


# Step 5: Automatically trigger after `generate_journal_webpage.py` finishes
def enhance_webpage(html_file_path):
    """
    Enhance the webpage by adding relevant images, matching fonts, adjusting readability, and adding a new background image.
    """
    html_content = fetch_html_file(html_file_path)

    if html_content:
        # Step 1: Add relevant images based on the journal content
        prompt = "Generate an image of people working on a tech project, representing progress in coding, debugging, and testing."
        enhanced_html = add_relevant_images(html_content, prompt)

        # Step 2: Add fonts from dadudekc.com
        enhanced_html = add_custom_fonts(enhanced_html)

        # Step 3: Update the background image
        enhanced_html = update_background_image(enhanced_html)

        # Step 4: Modify the HTML for better readability
        enhanced_html = modify_journal_html_for_readability(enhanced_html)

        # Save the enhanced HTML file
        enhanced_file_path = html_file_path.replace(".html", "_enhanced.html")
        with open(enhanced_file_path, 'w', encoding='utf-8') as file:
            file.write(enhanced_html)

        print(f"Enhanced HTML page saved successfully at {enhanced_file_path}")

if __name__ == "__main__":
    html_file_path = os.path.join(os.getcwd(), "project_journal_entry.html")
    
    # Automatically trigger enhancement after generate_journal_webpage.py
    if os.path.exists(html_file_path):
        enhance_webpage(html_file_path)
    else:
        print(f"Generated HTML file not found: {html_file_path}")
