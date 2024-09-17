
# Try importing GPT4Agent after dynamically adjusting sys.path
from GPT4Agent import GPT4Agent  # Import the GPT4Agent class

class DebuggerAgent(GPT4Agent):
    def __init__(self):
        super().__init__(name="Debugger", role="Debugging", personality="You are a debugging expert that can handle traceback errors.", task_function=self.debug_task_function)

    def debug_task_function(self, error_traceback):
        """
        Debugger agent iterates through fixing errors.
        """
        attempt = 1
        while True:
            print(f"Attempt {attempt}: Fixing error")
            # Simulate the generation of new code based on the error
            generated_fix = self.generate_fix(error_traceback)

            # Simulate testing the generated fix
            if self.test_fix(generated_fix):
                return f"Error fixed on attempt {attempt}: {generated_fix}"
            else:
                attempt += 1
                if attempt > 5:
                    return f"Unable to fix the error after {attempt} attempts."

    def generate_fix(self, error_traceback):
        # Generate new code based on the error
        return f"Generated fix based on error: {error_traceback}"

    def test_fix(self, generated_fix):
        # Simulate testing the generated fix
        return "Error" not in generated_fix
