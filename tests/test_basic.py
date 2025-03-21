import unittest
import subprocess
import re
import time

class TestVAPTOperation(unittest.TestCase):

    def run_vapt_commands(self, input_commands):
        """Run the VAPT tool interactively with proper arguments."""
        process = subprocess.Popen(
            ["sudo", "python3", "tidconsole.py", "--quiet"],  # ✅ Added "--quiet" to prevent test mode error
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Send multiple commands with slight delay to mimic user interaction
        output, error = process.communicate(input_commands)

        # Remove ANSI escape sequences (color codes, cursor moves, etc.)
        clean_output = re.sub(r'\x1b\[[0-9;]*[mHJK]', '', output)

        return clean_output, error

    def test_vapt_execution(self):
        """Test if the VAPT tool runs interactively and executes commands successfully."""
        input_commands = "?\nlist\nvicadd www.google.com\nlist osint-passive\nlist osint-active\nload getgeoip\nattack getgeoip\nexit\n"
        clean_output, error = self.run_vapt_commands(input_commands)

        # Print output for debugging
        print("==== CLEANED OUTPUT ====")
        print(clean_output)
        print("========================")

        # Validate expected output
        self.assertTrue(
            "help" in clean_output.lower() or "list" in clean_output.lower() or "victims" in clean_output.lower(),
            f"Expected CLI responses not found! Output received:\n{clean_output}"
        )

if __name__ == "__main__":
    unittest.main()

