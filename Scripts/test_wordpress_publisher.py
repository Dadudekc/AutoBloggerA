# -------------------------------------------------------------------
# File Path: C:\Auto_Blogger\Scripts\Tests\test_wordpress_publisher.py
# Description: Unit tests for the WordPress post-publishing script 
# (wordpress_publisher.py). These tests ensure that posts are correctly
# published and that error handling works as expected.
# -------------------------------------------------------------------

import unittest
from unittest.mock import patch
import requests
from wordpress_publisher import publish_to_wordpress

# -------------------------------------------------------------------
# Section 1: Test the WordPress Publisher
# -------------------------------------------------------------------
class TestWordPressPublisher(unittest.TestCase):

    @patch('wordpress_publisher.requests.post')
    def test_successful_publish(self, mock_post):
        """
        Test the publish_to_wordpress function for a successful post.
        Mock the requests.post method to simulate a successful API response.
        """
        # Simulate a successful response from the WordPress API
        mock_response = requests.Response()
        mock_response.status_code = 201  # HTTP 201 Created
        mock_post.return_value = mock_response

        # Example data for the post
        title = "Test Post"
        content = "<p>This is a test post content.</p>"

        # Call the function
        result = publish_to_wordpress(title, content, publish_in_days=3)

        # Assert that the result is True (successful publish)
        self.assertTrue(result, "Post should be published successfully")

        # Assert that the requests.post was called once
        mock_post.assert_called_once()

    @patch('wordpress_publisher.requests.post')
    def test_publish_failure(self, mock_post):
        """
        Test the publish_to_wordpress function for a failed post.
        Mock the requests.post method to simulate a failed API response.
        """
        # Simulate a failed response from the WordPress API
        mock_response = requests.Response()
        mock_response.status_code = 500  # HTTP 500 Internal Server Error
        mock_post.return_value = mock_response

        # Example data for the post
        title = "Test Post"
        content = "<p>This is a test post content.</p>"

        # Call the function
        result = publish_to_wordpress(title, content, publish_in_days=3)

        # Assert that the result is False (publish failed)
        self.assertFalse(result, "Post should fail to publish")

        # Assert that the requests.post was called once
        mock_post.assert_called_once()

    @patch('wordpress_publisher.requests.post')
    def test_publish_exception(self, mock_post):
        """
        Test the publish_to_wordpress function when an exception occurs
        during the requests.post call.
        """
        # Simulate an exception during the API call
        mock_post.side_effect = requests.exceptions.RequestException("Network error")

        # Example data for the post
        title = "Test Post"
        content = "<p>This is a test post content.</p>"

        # Call the function
        result = publish_to_wordpress(title, content, publish_in_days=3)

        # Assert that the result is False (exception occurred)
        self.assertFalse(result, "Post should fail due to network error")

        # Assert that the requests.post was called once
        mock_post.assert_called_once()

# -------------------------------------------------------------------
# Section 2: Run Unit Tests
# -------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main()
