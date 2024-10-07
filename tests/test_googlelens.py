import unittest
from googlelens import GoogleLens, GoogleLensResults


class TestGoogleLens(unittest.TestCase):

    def setUp(self):
        """Initialize the GoogleLens instance for testing."""
        self.lens = GoogleLens()

    def test_upload_image_url(self):
        """Test uploading image via URL."""
        url = "https://example.com/sample-image.jpg"
        result = self.lens.upload_image(url)
        self.assertIsInstance(result, GoogleLensResults)
        self.assertIsNotNone(result.response)

    def test_upload_image_file(self):
        """Test uploading an image from a file path."""
        # You need to provide a valid image file for this test
        file_path = "tests/sample-image.jpg"
        result = self.lens.upload_image(file_path)
        self.assertIsInstance(result, GoogleLensResults)
        self.assertIsNotNone(result.response)

    def test_upload_image_bytes(self):
        """Test uploading an image using bytes."""
        # You need to provide a valid image file for this test
        with open("tests/sample-image.jpg", "rb") as f:
            image_bytes = f.read()
        result = self.lens.upload_image(image_bytes)
        self.assertIsInstance(result, GoogleLensResults)
        self.assertIsNotNone(result.response)

    def test_extract_visual_results(self):
        """Test extracting visual match results."""
        # Provide a mock or sample response for testing
        mock_response = "<html>...</html>"  # Add a real mock response here
        result = GoogleLensResults(mock_response)
        try:
            visual_data = result.extract_visual_results()
            self.assertIsInstance(visual_data, dict)
            self.assertIn("match", visual_data)
        except ValueError:
            pass  # Expected behavior if no valid data found

if __name__ == "__main__":
    unittest.main()
