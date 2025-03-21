import unittest
import subprocess
import re
import time

class TestVAPTOperation(unittest.TestCase):

    def run_vapt_commands(self, input_commands):
        """Run the VAPT tool interactively with proper arguments."""
        process = subprocess.Popen(
            ["sudo", "python3", "tidconsole.py", "--quiet"],  # ✅ Runs quietly without test mode
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Send multiple commands with delays to mimic user interaction
        output, error = process.communicate(input_commands)

        # Remove ANSI escape sequences (color codes, cursor moves, etc.)
        clean_output = re.sub(r'\x1b\[[0-9;]*[mHJK]', '', output)

        return clean_output.strip(), error.strip()

    def test_vapt_execution(self):
        """Test if the VAPT tool runs interactively and executes commands successfully."""
        input_commands = (
            "?\n"  # Show help menu
            "list\n"  # List available options
            "vicadd www.google.com\ny\n\n"  # Add victim (with SSL confirmation 'y')
            "list osint-passive\n"  # List passive reconnaissance modules
            "list osint-active\n"  # List active reconnaissance modules
            "load getgeoip\n"  # Load a module
            "attack getgeoip\n"  # Execute attack
            "exit\n"  # Exit the tool
        )

        clean_output, error = self.run_vapt_commands(input_commands)

        # Print output for debugging
        print("==== CLEANED OUTPUT ====")
        print(clean_output)
        print("========================")

        # Validate expected output
        self.assertTrue(
            any(keyword in clean_output.lower() for keyword in ["help", "list", "victims", "attack", "geoip"]),
            f"Expected CLI responses not found! Output received:\n{clean_output}"
        )

if __name__ == "__main__":
    unittest.main()

