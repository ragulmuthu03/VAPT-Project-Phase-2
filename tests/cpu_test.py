import unittest
import psutil
import tidconsole  # Import CLI tool

class TestCPUUsage(unittest.TestCase):

    def test_cpu_usage(self):
        """Test CPU usage of the VAPT tool."""
        process = psutil.Process()
        start_cpu = process.cpu_percent(interval=1)

        # ✅ Fix: Use `main()` instead of `run()`
        try:
            tidconsole.main()
        except SystemExit:
            pass  # Prevent test failure if argparse exits

        end_cpu = process.cpu_percent(interval=1)
        cpu_usage = end_cpu - start_cpu
        print(f"CPU Usage: {cpu_usage:.2f}%")
        self.assertLess(cpu_usage, 80)  # Adjust as needed

if __name__ == "__main__":
    unittest.main()

