from memory_profiler import memory_usage
import unittest
import tidconsole

class TestMemoryUsage(unittest.TestCase):

    def test_memory_usage(self):
        mem_usage = memory_usage(tidconsole.run, interval=0.1)
        peak_memory = max(mem_usage)
        print(f"Peak Memory Usage: {peak_memory} MB")
        self.assertLess(peak_memory, 500)  # Example threshold

if __name__ == "__main__":
    unittest.main()

