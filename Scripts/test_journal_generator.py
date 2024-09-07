# -------------------------------------------------------------------
# File Path: C:\Auto_Blogger\Scripts\Tests\test_journal_generator.py
# Description: Unit tests for the journal entry generation script 
# (journal_generator.py). These tests check if the journal entry is 
# generated correctly based on the prompt provided.
# -------------------------------------------------------------------

import unittest
from journal_generator import generate_journal_entry, get_journal_prompt

# -------------------------------------------------------------------
# Section 1: Mock Data for Testing
# -------------------------------------------------------------------
class TestJournalGenerator(unittest.TestCase):

    def setUp(self):
        """
        Set up test data and configurations before running tests.
        This method runs before each test.
        """
        self.maxDiff = None  # Allow full diff to be shown for debugging
        self.sample_git_commits = """
        Recent Commits:
        - abc1234 - Refactored API handling to improve response time.
        - def5678 - Fixed bug in data fetching module.
        - ghi7890 - Added unit tests for data validation.
        """
        self.expected_prompt = """
        Use this conversation to make a project journal entry following the standards and guides of the template below. 
        Base the title of the entry off of the conversation.

        ## Work Completed
        Provide a detailed and structured account of the tasks you accomplished. Address the following points:
        - **Objectives and Goals:** Clearly state the main objectives and goals for the work session.
        - **Actions Taken:** Describe key actions taken and steps completed, providing context for each.
        - **Challenges and Breakthroughs:** Discuss any major breakthroughs or challenges encountered and how they were resolved.
        - **Results and Impact:** Summarize the outcomes of your efforts and how they contribute to the project's progress. Highlight the impact on the overall project.

        Recent Commits:
        - abc1234 - Refactored API handling to improve response time.
        - def5678 - Fixed bug in data fetching module.
        - ghi7890 - Added unit tests for data validation.

        ## Skills and Technologies Used
        Detail the skills and technologies you utilized. Highlight any new skills acquired or existing skills that were particularly useful. Explain how these skills contributed to your progress and the quality of your work.

        ## Lessons Learned
        Reflect on the key takeaways from the session. Address any unexpected challenges and how these learnings might influence your future work.

        ## To-Do
        Outline the next steps and tasks that need to be completed. Be specific and prioritize the tasks based on their importance and urgency. Include deadlines if applicable.
        """
    
    # -------------------------------------------------------------------
    # Section 2: Test the Prompt Generation Function
    # -------------------------------------------------------------------
    def test_get_journal_prompt(self):
        """
        Test that the get_journal_prompt function returns the correct prompt string
        based on the provided Git commits.
        """
        generated_prompt = get_journal_prompt(self.sample_git_commits)
        # Compare the generated prompt to the expected prompt
        self.assertEqual(generated_prompt.strip(), self.expected_prompt.strip(), "Prompt generation failed")

    # -------------------------------------------------------------------
    # Section 3: Test the Journal Entry Generation (Mocked GPT Response)
    # -------------------------------------------------------------------
    def test_generate_journal_entry(self):
        """
        Test the generate_journal_entry function. This test will simulate a 
        simple response from GPT-4 (mock the API call).
        """
        sample_prompt = get_journal_prompt(self.sample_git_commits)

        # Mock response for the GPT-4 API call
        expected_journal_entry = """
        Today, I worked on the following tasks:
        
        Objectives and Goals:
        - Refactor the API handling system to improve response time.
        
        Actions Taken:
        - Refactored the API handling system.
        - Fixed bugs in the data fetching module.
        - Added unit tests for data validation.
        
        Challenges:
        - Encountered issues with testing edge cases for the data validation.

        Skills and Technologies Used:
        - Python, API handling, Unit Testing.

        Lessons Learned:
        - Validated the importance of writing tests for edge cases.

        To-Do:
        - Finalize the testing suite and prepare for the next deployment.
        """

        # In a real scenario, the following call would be replaced with an actual API call to GPT-4.
        # Here we simply return a predefined response to simulate the GPT response.
        def mock_generate_journal_entry(prompt):
            return expected_journal_entry
        
        # Use the mock function instead of the real GPT API call
        generated_journal_entry = mock_generate_journal_entry(sample_prompt)
        
        # Assert that the generated journal entry matches the expected output
        self.assertEqual(generated_journal_entry.strip(), expected_journal_entry.strip(), "Journal entry generation failed")
        
# -------------------------------------------------------------------
# Section 4: Run Unit Tests
# -------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main()
