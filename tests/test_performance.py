import sys
import os
import time
import unittest

# Ensure the correct path is set for imports
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/../"))

import tidconsole  # Import CLI tool

class TestPerformance(unittest.TestCase):

    def test_execution_time(self):
        start_time = time.time()
        tidconsole.main()  # ✅ Correct function to call
        elapsed_time = time.time() - start_time
        print(f"Execution Time: {elapsed_time:.2f} seconds")
        self.assertLess(elapsed_time, 10)  # Adjust threshold if needed

if __name__ == "__main__":
    unittest.main()

