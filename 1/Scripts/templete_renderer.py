# -------------------------------------------------------------------
# File Path: scripts/template_renderer.py
# Description: Renders journal entries into an HTML template using Jinja2.
# -------------------------------------------------------------------

from jinja2 import Template

# -------------------------------------------------------------------
# Section 1: Render function to inject data into the template
# -------------------------------------------------------------------
def render_journal_entry(parsed_data):
    template_str = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Journal Entry - {{ date }}</title>
    </head>
    <body>
        <h1>Journal Entry - {{ date }}</h1>
        <p>{{ intro }}</p>
        <h2>Summary</h2>
        <p>{{ summary }}</p>

        <h2>Accomplishments</h2>
        <ul>
        {% for acc in accomplishments %}
            <li><strong>{{ acc.title }}:</strong> {{ acc.detail }}</li>
        {% endfor %}
        </ul>

        <h2>Challenges</h2>
        <ul>
        {% for challenge in challenges %}
            <li>{{ challenge }}</li>
        {% endfor %}
        </ul>
    </body>
    </html>
    """
    template = Template(template_str)
    return template.render(parsed_data)

# -------------------------------------------------------------------
# Example Usage (Main Section)
# -------------------------------------------------------------------
if __name__ == "__main__":
    parsed_data = {
        "date": "July 3, 2024",
        "intro": "Started fixing circular dependencies.",
        "summary": "Refactored the code for better modularity.",
        "accomplishments": [{"title": "Code Refactoring", "detail": "Removed circular dependencies."}],
        "challenges": ["Debugging issues", "Lack of comprehensive testing."],
        # Add more sections here
    }

    rendered_html = render_journal_entry(parsed_data)
    with open("journal_entry_july_3_2024.html", "w") as f:
        f.write(rendered_html)
