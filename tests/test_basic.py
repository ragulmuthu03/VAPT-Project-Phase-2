import unittest
import os
import subprocess

class TestVAPTOperation(unittest.TestCase):

    def test_vapt_execution(self):
        """Test if the VAPT tool runs without errors."""
        result = subprocess.run(["python3", "tidconsole.py", "--help"], capture_output=True, text=True)
        self.assertTrue("Vsynta.: tidos" in result.stdout or "--victim" in result.stdout or "--help" in result.stdout)


    def test_vapt_scan_example(self):
        """Run a basic scan on example.com"""
        result = subprocess.run(["python3", "tidconsole.py", "-v", "example.com", "-l", "scan.nmap"], capture_output=True, text=True)
        self.assertNotIn("Error", result.stderr)  # Ensure no errors occur

if __name__ == "__main__":
    unittest.main()

