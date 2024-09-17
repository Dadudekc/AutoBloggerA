
# Try importing GPT4Agent after dynamically adjusting sys.path
from GPT4Agent import GPT4Agent  # Import the GPT4Agent class

class JournalAgent(GPT4Agent):
    def __init__(self):
        super().__init__(
            name="JournalAgent",
            role="Journal Writing",
            personality="I am an expert in documentation and converting journal entries into structured content.",
            task_function=self.journal_task_function
        )

    def journal_task_function(self, json_data):
        """
        Converts the provided JSON journal entry into an HTML format.
        """
        html_content = []
        
        for item in json_data["content"]:
            if "heading" in item:
                html_content.append(f"<h2>{item['heading']}</h2>")
            elif "paragraph" in item:
                html_content.append(f"<p>{item['paragraph']}</p>")
            elif "unordered_list" in item:
                html_content.append("<ul>")
                for list_item in item["unordered_list"]:
                    html_content.append(f"<li>{list_item}</li>")
                html_content.append("</ul>")
        
        # Save the HTML content
        html_output = "\n".join(html_content)
        file_name = f"journal_entry_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        with open(f"/Auto_Blogger/Output/{file_name}", 'w') as html_file:
            html_file.write(f"<html><body>{html_output}</body></html>")
        
        return f"Journal entry converted to HTML and saved as {file_name}"

