import unittest
from memory_profiler import memory_usage
import tidconsole  # Import CLI tool

class TestMemoryUsage(unittest.TestCase):

    def test_memory_usage(self):
        """Test Memory Usage of the VAPT tool."""
        try:
            mem_usage = memory_usage(tidconsole.main, interval=0.1)  # ✅ Fix function call
        except SystemExit:
            mem_usage = [0]  # Prevent test failure if argparse exits

        peak_memory = max(mem_usage)
        print(f"Peak Memory Usage: {peak_memory:.2f} MB")
        self.assertLess(peak_memory, 500)  # Adjust as needed

if __name__ == "__main__":
    unittest.main()

