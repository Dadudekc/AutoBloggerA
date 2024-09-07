import os

# -------------------------------------------------------------------
# Section: Modify HTML for Dadudekc Website Post
# -------------------------------------------------------------------
def modify_html_for_dadudekc(original_html, background_image_path):
    """
    Modify the original journal entry HTML to match the style of a post from
    the dadudekc website.

    Args:
    - original_html (str): The original HTML content generated.
    - background_image_path (str): Path to the background image.

    Returns:
    - str: The modified HTML content.
    """
    # Define the new background style for the dadudekc post
    background_style = f"background: url('{background_image_path}') no-repeat center center fixed; opacity: 0.4;"

    # Modify the original HTML to match dadudekc style
    modified_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Journal Entry</title>
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
        {original_html}
    </body>
    </html>
    """
    return modified_html

# -------------------------------------------------------------------
# Example Usage (Main Section)
# -------------------------------------------------------------------
if __name__ == "__main__":
    # Example: Load the original HTML content from the generate_journal_html function
    original_html_content = """
        <h1>Untitled Journal Entry</h1>
        <div class="section">
            <h2>Session Prompt</h2>
            <p>No Session Prompt</p>
        </div>
        <div class="section">
            <h2>Work Completed</h2>
            <p>No Work Completed</p>
        </div>
        <div class="section">
            <h2>Skills and Technologies Used</h2>
            <p>No Skills or Technologies Listed</p>
        </div>
        <div class="section">
            <h2>Lessons Learned</h2>
            <p>No Lessons Learned</p>
        </div>
        <div class="section">
            <h2>To-Do</h2>
            <p>No To-Do List</p>
        </div>
        <div class="section">
            <h2>Additional Notes</h2>
            <p>No Additional Notes</p>
        </div>
        <div class="section">
            <h2>Project Milestones</h2>
            <ul></ul>
        </div>
    """

    # Path to the background image
    background_image_path = r"C:\Auto_Blogger\images\Untitled_Journal_Entry_20240907-041045.png"

    # Modify the HTML to match the dadudekc website style
    modified_html = modify_html_for_dadudekc(original_html_content, background_image_path)

    # Save the modified HTML
    output_path = os.path.join(os.getcwd(), "dadudekc_journal_entry.html")
    with open(output_path, "w") as f:
        f.write(modified_html)

    print(f"Modified HTML page saved successfully at {output_path}")
