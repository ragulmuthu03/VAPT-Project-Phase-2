import unittest
import os
import time
import psutil
import subprocess
import socket
import matplotlib.pyplot as plt
from memory_profiler import memory_usage

# Define target domain
DOMAIN = "example.com"

def get_ip(domain):
    """Convert domain to IP address"""
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None  # Return None if resolution fails

IP_ADDRESS = get_ip(DOMAIN)  # Convert domain to IP

class TestPerformance(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Ensure 'reports' directory exists before running tests."""
        os.makedirs("reports", exist_ok=True)

    def is_tool_installed(self, tool_name):
        """Check if a tool is installed"""
        return subprocess.call(f"which {tool_name}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0

    def measure_execution_time(self, command, input_commands="", timeout=20):
        """Run a command with automated user input and measure execution time"""
        start_time = time.time()
        try:
            process = subprocess.Popen(
                command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
                text=True
            )
            process.communicate(input=input_commands)  # ✅ Send user commands
        except subprocess.TimeoutExpired:
            print(f"⚠️ {command} took too long and was terminated.")
            return timeout
        return time.time() - start_time

    def test_vapt_performance(self):
        """Measure performance for VAPT Tool"""
        results = {}

        # Load VAPT modules and measure execution
        modules = {
            "Nmap Module": "load scan.nmap",
            "Subnet Module": "load scan.subnet",
            "GeoIP Module": "load osint-passive.getgeoip"
        }

        for module, command in modules.items():
            execution_time = self.measure_execution_time(
                f"python3 tidconsole.py",
                f"vicadd {DOMAIN}\n{command}\nattack\nexit\n"
            )
            results[module] = {"execution_time": execution_time}
            print(f"{module}: Time={execution_time:.2f}s")

        self.save_results(results, "reports/vapt_performance.txt")

    def test_other_tools_performance(self):
        """Measure performance for external tools"""
        results = {}

        tools = {
            "Nmap": f"nmap -sn {DOMAIN}",
            "Subnet Enumeration": f"ipcalc {IP_ADDRESS}" if IP_ADDRESS else "echo '⚠️ Could not resolve domain to IP'",
            "GeoIP Lookup": f"geoiplookup {DOMAIN}"
        }

        for tool, command in tools.items():
            execution_time = self.measure_execution_time(command, timeout=10)
            results[tool] = {"execution_time": execution_time}
            print(f"{tool}: Time={execution_time:.2f}s")

        self.save_results(results, "reports/tools_performance.txt")

    def save_results(self, results, filename):
        """Save performance results to a file"""
        with open(filename, "w") as f:
            for tool, data in results.items():
                f.write(f"{tool}: Execution Time: {data['execution_time']:.2f}s\n")

        print(f"✅ {filename} saved.")

if __name__ == "__main__":
    import sys
    mode = sys.argv[1] if len(sys.argv) > 1 else None
    suite = unittest.TestSuite()

    if mode == "--mode=vapt":
        suite.addTest(TestPerformance("test_vapt_performance"))
    elif mode == "--mode=tools":
        suite.addTest(TestPerformance("test_other_tools_performance"))
    else:
        suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestPerformance))

    runner = unittest.TextTestRunner()
    runner.run(suite)

