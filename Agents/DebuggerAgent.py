# -------------------------------------------------------------------
# File Path: C:\Auto_Blogger\Agents\DebuggerAgent.py
# Description: Tech Intern agent responsible for debugging, learning from
# both successes and failures, adapting its strategies over time, and
# integrating LLM suggestions.
# -------------------------------------------------------------------

from GPT4Agent import GPT4Agent  # Import the base GPT4Agent class
import json
import logging
import requests
import autopep8
import black
import os

# Initialize logging
log_file_path = r'C:\Auto_Blogger\Logs\tech_intern_log.log'
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Expanded Fix catalog for common errors
ERROR_FIX_CATALOG = {
    "NameError": "Ensure the variable is defined or imported before use.",
    "TypeError": "Check if variable types are compatible for the operation.",
    "AttributeError": "Ensure the object has the correct attribute.",
    "KeyError": "Check if the key exists in the dictionary before accessing.",
    "IndexError": "Ensure the index is within the range of the list.",
    "ImportError": "Verify that the module is installed and imported correctly.",
    "SyntaxError": "Check for missing colons, parentheses, or indentation.",
    "ValueError": "Ensure the variable value is valid for the operation.",
    "IndentationError": "Check that the code follows proper indentation.",
    "ZeroDivisionError": "Ensure you are not dividing by zero.",
    "RecursionError": "Ensure there is a base case to stop the recursion.",
    "FileNotFoundError": "Check that the file path is correct and the file exists.",
}

# -------------------------------------------------------------------
# Class Definition: Tech Intern (DebuggerAgent)
# -------------------------------------------------------------------

class TechIntern(GPT4Agent):
    def __init__(self, shared_fix_history):
        super().__init__(
            name="Tech Intern", 
            role="Debugging Expert", 
            personality=(
                "A meticulous and relentless agent, focused on resolving code issues, "
                "learning from past mistakes, and ensuring system reliability."
            ),
            task_function=self.debug_task_function
        )
        self.shared_fix_history = shared_fix_history  # Shared fix history for collaboration

    # -------------------------------------------------------------------
    # Section 1: Debug Task Function
    # -------------------------------------------------------------------

    def debug_task_function(self, error_traceback):
        llm_response = self.query_llm_for_fix(error_traceback)
        if llm_response:
            if self.apply_fix(llm_response):
                logging.info(f"Fix applied using LLM suggestion: {llm_response}")
                return f"Fix applied using LLM suggestion: {llm_response}"

        fix_from_history = self.query_fix_history(error_traceback)
        if fix_from_history:
            logging.info(f"Fix found in shared history: {fix_from_history}")
            return fix_from_history

        attempt = 1
        while attempt <= 5:
            logging.info(f"Attempt {attempt}: Debugging error {error_traceback}")
            generated_fix = self.generate_fix(error_traceback)

            if self.test_fix(generated_fix):
                self.save_fix_to_history(error_traceback, generated_fix, success=True)
                self.apply_fix(generated_fix)  # Apply fix here
                return f"Error fixed on attempt {attempt}: {generated_fix}"
            attempt += 1

        return self.escalate_issue(error_traceback)

    # -------------------------------------------------------------------
    # Section 2: Apply Fix
    # -------------------------------------------------------------------

    def apply_fix(self, fix):
        """
        Apply the suggested fix to the code file.
        """
        # Assuming the error traceback contains the file path and line number
        file_path = "path/to/your/file.py"  # Specify the correct file path
        line_number = 10  # Replace with the actual line number where the error occurs
        
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()

            # Apply the fix to the specific line
            lines[line_number - 1] = f"{lines[line_number - 1].strip()}  # {fix}\n"  # Comment the fix

            with open(file_path, 'w') as file:
                file.writelines(lines)

            logging.info(f"Applied fix to {file_path} at line {line_number}: {fix}")
            return True  # Return True if the fix was applied successfully
        except Exception as e:
            logging.error(f"Failed to apply fix to {file_path}: {e}")
            return False  # Return False if the fix could not be applied

    # -------------------------------------------------------------------
    # Section 2: Query LLM for Fix
    # -------------------------------------------------------------------

    def query_llm_for_fix(self, error_traceback):
        """
        Query a free LLM for a suggested fix based on the error traceback.
        """
        # Example API endpoint for the LLM
        llm_api_url = "https://api.example.com/chatgpt"  # Replace with actual API URL
        payload = {"input": error_traceback}

        try:
            response = requests.post(llm_api_url, json=payload)
            response.raise_for_status()
            return response.json().get("suggested_fix")
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to get response from LLM: {e}")
            return None

    # -------------------------------------------------------------------
    # Section 3: Apply Fix
    # -------------------------------------------------------------------

    def apply_fix(self, fix):
        """
        Apply the suggested fix to the code file.
        """
        # Placeholder: Implement logic to modify the source code based on the fix.
        logging.info(f"Applying fix: {fix}")
        # For now, we'll simulate that the fix is applied successfully.
        return True  # Return True if fix was applied successfully

    # -------------------------------------------------------------------
    # Section 4: Generate Fix
    # -------------------------------------------------------------------

    def generate_fix(self, error_traceback):
        """
        Generate a fix based on the error traceback by consulting the fix catalog.
        """
        for error_type, fix in ERROR_FIX_CATALOG.items():
            if error_type in error_traceback:
                logging.info(f"Fix suggestion: {fix}")
                return fix

        # Default response if error type is not found
        return "No known fix found. Try alternative debugging strategies."

    # -------------------------------------------------------------------
    # Section 5: Query and Save Fix History
    # -------------------------------------------------------------------

    def query_fix_history(self, error_traceback):
        """
        Query the shared fix history to see if a solution already exists.
        """
        for entry in self.shared_fix_history:
            # Check if the required fields exist in the entry
            if "error_traceback" in entry and "generated_fix" in entry and "success" in entry:
                if entry["error_traceback"] == error_traceback and entry["success"]:
                    return entry["generated_fix"]
            else:
                logging.warning(f"Invalid entry in fix history: {entry}")
        return None

    def save_fix_to_history(self, error_traceback, generated_fix, success):
        """
        Save successful or failed fixes to a shared fix history for future reference.
        """
        fix_entry = {
            "error_traceback": error_traceback,
            "generated_fix": generated_fix,
            "success": success
        }

        # Save the fix to the shared history
        self.shared_fix_history.append(fix_entry)

        # Also save to the shared JSON file for persistence
        fix_history_file = r'C:\Auto_Blogger\Agents\Data\fix_history.json'
        with open(fix_history_file, 'w') as file:
            json.dump(self.shared_fix_history, file, indent=4)

        logging.info(f"Fix {'successful' if success else 'failed'} saved for {error_traceback}")

    # -------------------------------------------------------------------
    # Section 6: Test Fix
    # -------------------------------------------------------------------

    def test_fix(self, generated_fix):
        """
        Simulate testing the generated fix. Returns True if the fix is successful.
        """
        logging.info(f"Testing fix: {generated_fix}")
        # Simulate successful fix testing
        return "Error" not in generated_fix

    # -------------------------------------------------------------------
    # Section 7: Escalate Issue
    # -------------------------------------------------------------------

    def escalate_issue(self, error_traceback):
        """
        Escalate issue by refining the fix strategy or applying external refactoring tools.
        """
        logging.warning(f"Escalating issue for traceback: {error_traceback}")

        # Check external sources (e.g., Stack Overflow)
        documentation_fix = self.consult_external_sources(error_traceback)
        if documentation_fix:
            return documentation_fix

        # Apply advanced refactoring tools
        refactored_code = self.apply_advanced_refactoring(error_traceback)
        if refactored_code:
            return refactored_code

        # Last resort: Escalate to senior developer or report the issue
        escalation_report = {
            "Error Traceback": error_traceback,
            "Attempts Made": 5,
            "Suggested Fix": "Refactor problematic code or escalate to senior developer."
        }
        logging.error(f"Unable to fix error after multiple attempts. Escalation Report: {escalation_report}")
        return f"Escalation Report: {escalation_report}"

    # -------------------------------------------------------------------
    # Section 8: External Sources and Refactoring
    # -------------------------------------------------------------------

    def consult_external_sources(self, error_traceback):
        """
        Check external sources (e.g., Stack Overflow) for solutions to the error.
        """
        logging.info(f"Consulting external sources for: {error_traceback}")

        query = error_traceback.split(":")[0]  # Extract error type (e.g., NameError)
        url = (
            f"https://api.stackexchange.com/2.2/search/advanced?"
            f"order=desc&sort=relevance&q={query}&site=stackoverflow"
        )
        try:
            response = requests.get(url)
            response.raise_for_status()
            results = response.json().get("items", [])
            if results:
                top_answer = results[0].get("link")
                logging.info(f"Found Stack Overflow solution: {top_answer}")
                return f"Solution found on Stack Overflow: {top_answer}"
        except requests.exceptions.RequestException as e:
            logging.error(f"Error querying external sources: {e}")

        logging.error("No relevant solution found from external sources.")
        return None

    def apply_advanced_refactoring(self, error_traceback):
        """
        Apply refactoring tools such as black or autopep8 to the code.
        """
        logging.info(f"Applying advanced refactoring to: {error_traceback}")

        # Simulate using autopep8 for formatting
        try:
            refactored_code = autopep8.fix_code(error_traceback)
            if refactored_code:
                logging.info(f"Refactored code with autopep8: {refactored_code}")
                return refactored_code
        except Exception as e:
            logging.error(f"autopep8 failed: {e}")

        # Use black for deeper formatting if autopep8 doesn't suffice
        try:
            refactored_code = black.format_str(error_traceback, mode=black.Mode())
            logging.info(f"Refactored code with black: {refactored_code}")
            return refactored_code
        except (black.parsing.InvalidInput, Exception) as e:
            logging.error(f"Black formatting failed: {e}")
            return None

# -------------------------------------------------------------------
# Example Usage (Main Section)
# -------------------------------------------------------------------


if __name__ == "__main__":
    shared_fix_history_file = r'C:\Auto_Blogger\Agents\Data\fix_history.json'
    try:
        with open(shared_fix_history_file, 'r') as file:
            shared_fix_history = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        shared_fix_history = []

    tech_intern = TechIntern(shared_fix_history)
    print(tech_intern.introduce())

    result = tech_intern.perform_task("NameError: name 'x' is not defined")
    print(result)