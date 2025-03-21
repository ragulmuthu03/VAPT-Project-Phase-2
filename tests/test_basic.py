import unittest
import subprocess
import re

class TestVAPTOperation(unittest.TestCase):

    def test_vapt_execution(self):
        """Test if the VAPT tool runs without errors and displays correct output."""
        result = subprocess.run(
            ["python3", "tidconsole.py", "--help"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Remove ANSI escape sequences
        clean_output = re.sub(r'\x1b\[[0-9;]*[mHJK]', '', result.stdout)

        # Print output for debugging
        print("==== CLEANED OUTPUT ====")
        print(clean_output)
        print("========================")

        # Validate expected output exists
        self.assertTrue("tidos" in clean_output.lower() or "-v vic" in clean_output.lower() or "--victim" in clean_output.lower(),
                        f"Expected keywords not found in output! Output received:\n{clean_output}")

if __name__ == "__main__":
    unittest.main()

