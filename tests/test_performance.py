import time
import unittest
import tidconsole

class TestPerformance(unittest.TestCase):

    def test_execution_time(self):
        start_time = time.time()
        tidconsole.run()  # Run CLI tool
        elapsed_time = time.time() - start_time
        print(f"Execution Time: {elapsed_time:.2f} seconds")
        self.assertLess(elapsed_time, 10)  # Example threshold

if __name__ == "__main__":
    unittest.main()

