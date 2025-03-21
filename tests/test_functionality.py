import unittest
from tidconsole import main

class TestFunctionality(unittest.TestCase):

    def test_function_execution(self):
        """Test if the main function runs without errors"""
        try:
            main()
            self.assertTrue(True)  # Pass if no errors
        except Exception as e:
            self.fail(f"Function execution failed: {e}")

if __name__ == "__main__":
    unittest.main()

