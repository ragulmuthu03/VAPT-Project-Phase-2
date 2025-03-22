import unittest
import subprocess
import re
import time

class TestVAPTOperation(unittest.TestCase):

    def run_vapt_commands(self, input_commands):
        """Run the VAPT tool interactively and capture output."""
        process = subprocess.Popen(
            ["sudo", "python3", "tidconsole.py", "--quiet"],  # ✅ Ensure proper execution
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Introduce a slight delay to allow CLI initialization
        time.sleep(2)

        # Send commands with simulated user input
        output, error = process.communicate(input_commands)

        # Remove ANSI escape sequences (color codes, cursor moves, etc.)
        clean_output = re.sub(r'\x1b\[[0-9;]*[mHJK]', '', output)

        return clean_output, error

    def test_vapt_execution(self):
        """Test if the VAPT tool runs and processes commands successfully."""
        input_commands = (
            "?\n"  # List available commands
            "list\n"  # List all categories
            "vicadd www.google.com\n"  # Add victim
            "list osint-passive\n"  # List passive reconnaissance modules
            "load getgeoip\n"  # Load GeoIP lookup module
            "attack\n"  # Run attack
            "exit\n"  # Exit the tool
        )

        clean_output, error = self.run_vapt_commands(input_commands)

        # Print output for debugging
        print("==== CLEANED OUTPUT ====")
        print(clean_output)
        print("========================")

        # Validate expected output
        expected_keywords = ["help", "list", "vicadd", "attack", "geoip", "exit"]
        self.assertTrue(
            any(keyword in clean_output.lower() for keyword in expected_keywords),
            f"Expected CLI responses not found! Output received:\n{clean_output}"
        )

if __name__ == "__main__":
    unittest.main()

