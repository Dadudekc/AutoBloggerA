# -------------------------------------------------------------------
# File Path: Scripts/generate_journal_webpage.py
# Description: Generates a project journal entry webpage with dynamic
# backgrounds and styling based on the journal entry content.
# -------------------------------------------------------------------

import os
import openai
import requests
import configparser
import time
import json
import html

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

# Step 1: Fetch journal entry dynamically from a directory
def fetch_journal_entry(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        print(f"Error fetching journal entry: {e}")
        return None

# Step 2: Use OpenAI to extract journal sections based on user's preferred tone
def extract_journal_sections_with_openai(journal_entry_text):
    """
    Extract journal sections using OpenAI. Returns the sections in a way that conveys
    the user's professional, relatable tone.

    Args:
    - journal_entry_text (str): The full text of the journal entry.

    Returns:
    - dict: A dictionary containing the extracted sections.
    """
    try:
        # Construct the chat-style message for GPT-4
        messages = [
            {"role": "system", "content": "You are a helpful assistant that extracts sections from journal entries."},
            {"role": "user", "content": f"""
            I have a project journal entry that I need turned into a webpage, and I want the style to reflect how I speak: 
            professional but easy to understand, conversational, and relatable. Please extract the following sections:
            1. Title
            2. Session Prompt
            3. Work Completed
            4. Skills and Technologies Used
            5. Lessons Learned
            6. To-Do
            7. Additional Notes
            8. Project Milestones

            Journal Entry:
            {journal_entry_text}

            Return the result as a JSON object with the section titles as keys.
            """}
        ]

        # Use the OpenAI chat completion endpoint
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            max_tokens=1500,
            n=1,
            temperature=0.5
        )

        extracted_sections = response['choices'][0]['message']['content'].strip()
        
        try:
            return json.loads(extracted_sections)
        except json.JSONDecodeError:
            print("Error decoding JSON from OpenAI response.")
            return {}
        
    except Exception as e:
        print(f"Error during OpenAI request: {e}")
        return None

# Step 3: Generate and save DALL·E image based on the prompt
def generate_and_save_dalle_image(image_prompt, entry_title):
    """
    Generate a DALL·E image based on the prompt and save it dynamically into the images folder with a unique name.

    Args:
    - image_prompt (str): The prompt to generate the image.
    - entry_title (str): The journal entry title, used to name the image.

    Returns:
    - str: The path to the saved image.
    """
    try:
        response = openai.Image.create(prompt=image_prompt, n=1, size="1024x1024")
        image_url = response['data'][0]['url']

        timestamp = time.strftime("%Y%m%d-%H%M%S")
        image_filename = f"{entry_title.replace(' ', '_')}_{timestamp}.png"
        image_path = os.path.join(images_folder, image_filename)

        image_data = requests.get(image_url).content
        with open(image_path, 'wb') as handler:
            handler.write(image_data)

        print(f"Image saved successfully at {image_path}")
        return image_path

    except Exception as e:
        print(f"Error generating or saving image: {e}")
        return None

# Step 4: Generate the HTML for the journal entry with the background

def clean_text(text):
    """
    Clean the input text by removing unnecessary line breaks, extra spaces, or special characters that could break the HTML.
    Additionally, it handles nested dictionaries and lists gracefully.
    """
    if isinstance(text, dict):
        # If it's a dictionary, flatten it into a readable string
        return " ".join([f"{key}: {value}" for key, value in text.items()])
    elif isinstance(text, list):
        # If it's a list, join items into a string
        return " ".join(text)
    elif isinstance(text, str):
        return " ".join(text.split()).replace("\n", " ").strip()
    else:
        return str(text)  # Convert other types to string safely

def format_html_paragraph(items, is_list=False):
    """
    Convert a list of items into an HTML paragraph or list format, handling empty cases gracefully.
    Also handles nested dictionaries by extracting their string values.
    """
    if not items:
        return ""
    
    # If it's a dictionary, flatten it into a list of key-value pairs
    if isinstance(items, dict):
        items = [f"{key}: {value}" for key, value in items.items()]
    
    # If items is still not a list (e.g., it's a string), treat it as a single element list
    if not isinstance(items, list):
        items = [items]
    
    if is_list:
        formatted_items = "".join([f"<li>{html.escape(clean_text(item))}</li>" for item in items])
        return f"<ul>{formatted_items}</ul>"
    else:
        return "<br>".join([html.escape(clean_text(item)) for item in items])

def generate_journal_html(title, session_prompt, work_completed, skills_used, lessons_learned, todo, notes, milestones, background_image_path):
    """
    Generates HTML content for the project journal entry with a background image at 40% opacity.
    Args:
    - title (str): The title of the journal entry.
    - session_prompt (str): The session details.
    - work_completed (list or dict): Work completed during the session, can be a list or dict.
    - skills_used (list or dict): Skills and technologies used.
    - lessons_learned (list or dict): Lessons learned during the project.
    - todo (list or dict): Tasks to be completed next.
    - notes (list or dict): Additional notes or challenges.
    - milestones (list or dict): Project milestones achieved.
    - background_image_path (str): Path to the background image.
    
    Returns:
    - str: HTML content string.
    """
    # Handle optional background image
    background_style = f"background: url('{background_image_path}') no-repeat center center fixed; opacity: 0.4;" if background_image_path else ""

    # Clean and format content
    session_prompt_clean = html.escape(clean_text(session_prompt))
    formatted_work_completed = format_html_paragraph(work_completed)
    formatted_skills = format_html_paragraph(skills_used, is_list=True)
    formatted_lessons = format_html_paragraph(lessons_learned)
    formatted_todo = format_html_paragraph(todo, is_list=True)
    formatted_notes = format_html_paragraph(notes)
    formatted_milestones = format_html_paragraph(milestones)

    # Build HTML sections
    sections = [
        generate_html_section("Session Prompt", session_prompt_clean),
        generate_html_section("Work Completed", formatted_work_completed),
        generate_html_section("Skills and Technologies Used", formatted_skills, is_list=True),
        generate_html_section("Lessons Learned", formatted_lessons),
        generate_html_section("To-Do", formatted_todo, is_list=True),
        generate_html_section("Additional Notes", formatted_notes),
        generate_html_section("Project Milestones", formatted_milestones)
    ]

    # Combine sections and generate final HTML
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{html.escape(title)}</title>
        <style>
            body {{
                font-family: 'Helvetica Neue', Arial, sans-serif;
                color: black;
                {background_style}
                background-size: cover;
                padding: 20px;
                max-width: 1200px;
                margin: auto;
            }}
            h1 {{
                text-align: center;
                font-size: 3em;
                margin-bottom: 20px;
            }}
            .section {{
                background-color: rgba(255, 255, 255, 0.8);
                padding: 20px;
                border-radius: 15px;
                margin-bottom: 20px;
            }}
            .section h2 {{
                font-size: 2em;
                color: #3498db;
                text-transform: uppercase;
                margin-bottom: 10px;
                border-bottom: 1px solid #ccc;
                padding-bottom: 10px;
            }}
            p {{
                line-height: 1.6;
            }}
            ul {{
                list-style-type: disc;
                margin-left: 20px;
            }}
        </style>
    </head>
    <body>
        <h1>{html.escape(title)}</h1>
        {"".join(sections)}
    </body>
    </html>
    """
    return html_content

def generate_html_section(title, content, is_list=False):
    """
    Generates an HTML section with a title and content. The content can be a list or paragraph.
    Args:
    - title (str): The section title.
    - content (str): The section content (already formatted).
    - is_list (bool): Whether the content is a list.
    
    Returns:
    - str: The formatted HTML section.
    """
    if not content:
        return ""  # Skip empty sections
    
    return f"""
    <div class="section">
        <h2>{html.escape(title)}</h2>
        {content}
    </div>
    """


# -------------------------------------------------------------------
# Section: Create Image Prompt Function
# -------------------------------------------------------------------

def create_image_prompt(journal_entry):
    """
    Create a summarized prompt for generating a background image, similar to
    the ones used on dadudekc.com. The prompt is based on the journal entry content.

    Args:
    - journal_entry (dict): The extracted journal entry sections.

    Returns:
    - str: The generated prompt for DALL·E.
    """
    title = journal_entry.get("Title", "Project Journal Entry")
    # Summarize the main themes in Work Completed, ensuring the prompt remains short
    main_theme = "Work progress and project management"
    style = "clean, minimal, professional"
    color_scheme = "dark, with muted tones"
    website = "tradingroboplug.com"
    
    return (f"Design a background image for my website {website} that reflects the theme of {main_theme}. "
            f"The style should be {style} with {color_scheme}. "
            f"The image will be used for a journal entry titled '{title}' and should have a 40% opacity.")

# Fetch the correct keys from the journal entry with case-sensitive keys
def get_journal_title(journal_entry):
    return journal_entry.get('Title', 'Untitled Journal Entry')

# Generate the HTML page with correct key references from OpenAI response
if __name__ == "__main__":
    file_path = r"C:\Auto_Blogger\Scripts\Journal\week 1\week 1 entry 2 07 - 6 - 2024"
    journal_entry_text = fetch_journal_entry(file_path)

    if journal_entry_text:
        journal_entry = extract_journal_sections_with_openai(journal_entry_text)

        # Debugging: Check the content of the extracted journal entry
        print(json.dumps(journal_entry, indent=4))

        if journal_entry:
            # Fetch the journal title with a fallback
            entry_title = get_journal_title(journal_entry)
            image_prompt = create_image_prompt(journal_entry)
            background_image_path = generate_and_save_dalle_image(image_prompt, entry_title)

            if background_image_path:
                # Adjust work_completed to handle it as a string
                html_content = generate_journal_html(
                    title=entry_title,
                    session_prompt=journal_entry.get('Session Prompt', 'No Session Prompt'),
                    work_completed=journal_entry.get('Work Completed', 'No Work Completed'),
                    skills_used=journal_entry.get('Skills and Technologies Used', 'No Skills or Technologies Listed'),
                    lessons_learned=journal_entry.get('Lessons Learned', 'No Lessons Learned'),
                    todo=journal_entry.get('To-Do', 'No To-Do List'),
                    notes=journal_entry.get('Additional Notes', 'No Additional Notes'),
                    milestones=journal_entry.get('Project Milestones', 'No Milestones'),
                    background_image_path=background_image_path
                )

                output_path = os.path.join(os.getcwd(), "project_journal_entry.html")
                with open(output_path, "w") as f:
                    f.write(html_content)

                print(f"HTML page generated successfully at {output_path}")
            else:
                print("Failed to generate the background image.")
        else:
            print("Failed to extract journal sections.")
    else:
        print("Failed to retrieve the journal entry.")
