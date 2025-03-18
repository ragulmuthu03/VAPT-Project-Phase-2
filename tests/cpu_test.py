import psutil
import unittest
import tidconsole
import time

class TestCPUUsage(unittest.TestCase):

    def test_cpu_usage(self):
        process = psutil.Process()
        start_cpu = process.cpu_percent(interval=1)

        tidconsole.run()  # Run CLI tool

        end_cpu = process.cpu_percent(interval=1)
        cpu_usage = end_cpu - start_cpu
        print(f"CPU Usage: {cpu_usage:.2f}%")
        self.assertLess(cpu_usage, 80)  # Example threshold

if __name__ == "__main__":
    unittest.main()

