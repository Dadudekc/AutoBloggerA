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
if not os.path.exists(images_folder):
    os.makedirs(images_folder)

# Fetch journal entry dynamically from a directory
def fetch_journal_entry(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        print(f"Error fetching journal entry: {e}")
        return None

# Extract detailed journal sections using OpenAI
def extract_journal_sections_with_openai(journal_entry_text):
    """
    Extract detailed journal sections using OpenAI. Returns the sections in a way that conveys
    the user's professional, relatable tone and provides a more comprehensive breakdown.

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
            6. Challenges Faced
            7. Solutions/Problem-Solving Approaches
            8. Key Takeaways
            9. Next Steps
            10. Additional Notes
            11. Important Dates
            12. Project Milestones

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
            temperature=0.5
        )

        # Extract raw response
        raw_response = response['choices'][0]['message']['content'].strip()
        print(f"Raw response from OpenAI:\n{raw_response}")  # Debugging line to print response

        try:
            return json.loads(raw_response)
        except json.JSONDecodeError as json_err:
            print(f"JSON decoding error: {json_err}")
            return {}

    except Exception as e:
        print(f"Error during OpenAI request: {e}")
        return None


# Generate and save DALL·E image based on the prompt
def generate_and_save_dalle_image(image_prompt, entry_title):
    try:
        response = openai.Image.create(prompt=image_prompt, n=1, size="1024x1024")
        image_url = response['data'][0]['url']
        image_filename = f"{entry_title.replace(' ', '_')}_{time.strftime('%Y%m%d-%H%M%S')}.png"
        image_path = os.path.join(images_folder, image_filename)
        image_data = requests.get(image_url).content
        with open(image_path, 'wb') as handler:
            handler.write(image_data)
        print(f"Image saved successfully at {image_path}")
        return image_path
    except Exception as e:
        print(f"Error generating or saving image: {e}")
        return None

# Helper function to clean and format text
def clean_text(text):
    if isinstance(text, dict):
        return " ".join([f"{key}: {value}" for key, value in text.items()])
    elif isinstance(text, list):
        return " ".join(text)
    elif isinstance(text, str):
        return " ".join(text.split()).replace("\n", " ").strip()
    else:
        return str(text)

# Helper function to format paragraphs or lists for HTML
def format_html_paragraph(items, is_list=False):
    if not items:
        return ""
    if isinstance(items, dict):
        items = [f"{key}: {value}" for key, value in items.items()]
    if not isinstance(items, list):
        items = [items]
    if is_list:
        return f"<ul>{''.join([f'<li>{html.escape(clean_text(item))}</li>' for item in items])}</ul>"
    else:
        return "<br>".join([html.escape(clean_text(item)) for item in items])

# Function to generate HTML for the journal entry
def generate_journal_html(title, session_prompt, work_completed, skills_used, lessons_learned, challenges_faced, solutions, key_takeaways, next_steps, notes, important_dates, milestones, background_image_path):
    sections = [
        generate_html_section("Session Prompt", html.escape(clean_text(session_prompt))),
        generate_html_section("Work Completed", format_html_paragraph(work_completed)),
        generate_html_section("Skills and Technologies Used", format_html_paragraph(skills_used, is_list=True)),
        generate_html_section("Lessons Learned", format_html_paragraph(lessons_learned)),
        generate_html_section("Challenges Faced", format_html_paragraph(challenges_faced)),
        generate_html_section("Solutions/Problem-Solving Approaches", format_html_paragraph(solutions)),
        generate_html_section("Key Takeaways", format_html_paragraph(key_takeaways)),
        generate_html_section("Next Steps", format_html_paragraph(next_steps, is_list=True)),
        generate_html_section("Additional Notes", format_html_paragraph(notes)),
        generate_html_section("Important Dates", format_html_paragraph(important_dates)),
        generate_html_section("Project Milestones", format_html_paragraph(milestones))
    ]

    return f"""
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
                background: url('{background_image_path}') no-repeat center center fixed;
                background-size: cover;
                padding: 20px;
                max-width: 1200px;
                margin: auto;
                position: relative;
            }}
            .overlay {{
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(255, 255, 255, 0.6);
                z-index: -1;
            }}
            h1 {{
                text-align: center;
                font-size: 3em;
                margin-bottom: 20px;
                color: #333;
            }}
            .section {{
                background-color: rgba(255, 255, 255, 0.9);
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 20px;
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
            }}
            .section h2 {{
                font-size: 2em;
                color: #3498db;
                margin-bottom: 10px;
            }}
            p {{
                line-height: 1.8;
                font-size: 1.1em;
            }}
            ul {{
                list-style-type: disc;
                margin-left: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="overlay"></div>
        <h1>{html.escape(title)}</h1>
        {"".join(sections)}
    </body>
    </html>
    """

# Helper function to generate each HTML section
def generate_html_section(title, content):
    if not content:
        return ""
    return f"""
    <div class="section">
        <h2>{html.escape(title)}</h2>
        {content}
    </div>
    """

# Function to create an image prompt
def create_image_prompt(journal_entry):
    title = journal_entry.get("Title", "Project Journal Entry")
    work_completed = journal_entry.get("Work Completed", "")
    if isinstance(work_completed, list):
        work_completed_clean = " ".join([" ".join(f"{k}: {v}" for k, v in item.items()) if isinstance(item, dict) else str(item) for item in work_completed])
    else:
        work_completed_clean = str(work_completed)

    work_completed_summary = (work_completed_clean[:200] + "...") if len(work_completed_clean) > 200 else work_completed_clean
    return f"Design an abstract, dark, clean, minimal, professional background image for a journal entry titled '{title}'. The theme is {work_completed_summary}. Use dark muted tones and tech-related visuals."

# Main functionality
if __name__ == "__main__":
    file_path = r"C:\Auto_Blogger\Scripts\Journal\week 1\week 1 entry 3 07 - 7 - 2024"
    journal_entry_text = fetch_journal_entry(file_path)

    if journal_entry_text:
        journal_entry = extract_journal_sections_with_openai(journal_entry_text)

        if journal_entry:
            entry_title = journal_entry.get('Title', 'Untitled Journal Entry')
            image_prompt = create_image_prompt(journal_entry)
            background_image_path = generate_and_save_dalle_image(image_prompt, entry_title)

            if background_image_path:
                html_content = generate_journal_html(
                    title=entry_title,
                    session_prompt=journal_entry.get('Session Prompt', 'No Session Prompt'),
                    work_completed=journal_entry.get('Work Completed', 'No Work Completed'),
                    skills_used=journal_entry.get('Skills and Technologies Used', 'No Skills Listed'),
                    lessons_learned=journal_entry.get('Lessons Learned', 'No Lessons Learned'),
                    challenges_faced=journal_entry.get('Challenges Faced', 'No Challenges Faced'),
                    solutions=journal_entry.get('Solutions/Problem-Solving Approaches', 'No Solutions Listed'),
                    key_takeaways=journal_entry.get('Key Takeaways', 'No Key Takeaways'),
                    next_steps=journal_entry.get('Next Steps', 'No Next Steps'),
                    notes=journal_entry.get('Additional Notes', 'No Additional Notes'),
                    important_dates=journal_entry.get('Important Dates', 'No Important Dates'),
                    milestones=journal_entry.get('Project Milestones', 'No Milestones'),
                    background_image_path=background_image_path
                )

                output_path = os.path.join(os.getcwd(), "project_journal_entry.html")
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(html_content)

                print(f"HTML page generated successfully at {output_path}")
            else:
                print("Failed to generate the background image.")
        else:
            print("Failed to extract journal sections.")
    else:
        print("Failed to retrieve the journal entry.")
