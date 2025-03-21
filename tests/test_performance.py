import unittest
import os
import time
import psutil
import subprocess
import matplotlib.pyplot as plt
from memory_profiler import memory_usage

DOMAIN = "example.com"  # ✅ Set target domain

def ensure_reports_directory():
    """Ensure the 'reports' directory exists before writing files."""
    os.makedirs("reports", exist_ok=True)

class TestPerformance(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Ensure 'reports' directory exists before running tests."""
        ensure_reports_directory()

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
        """Measure VAPT Tool Performance"""
        vapt_command = "python3 tidconsole.py"
        vapt_input = "help\nlist osint-passive\nload getgeoip\nattack getgeoip\nexit\n"
        vapt_execution_time = self.measure_execution_time(vapt_command, vapt_input, timeout=20)

        # Simulate CPU and memory usage
        vapt_cpu_usage = psutil.cpu_percent(interval=1)
        vapt_memory_usage = max(memory_usage((self.measure_execution_time, (vapt_command, vapt_input, 20))))

        # Save VAPT performance results
        ensure_reports_directory()
        with open("reports/vapt_performance.txt", "w") as f:
            f.write("VAPT Tool Performance Results\n")
            f.write(f"Execution Time: {vapt_execution_time:.2f}s\n")
            f.write(f"CPU Usage: {vapt_cpu_usage:.2f}%\n")
            f.write(f"Memory Usage: {vapt_memory_usage:.2f}MB\n")

        print("✅ VAPT performance results saved.")

    def test_other_tools_performance(self):
        """Compare VAPT Tool Against Other Security Tools"""

        tools = {
            "Nmap": f"nmap -sn {DOMAIN}",
            "WhatWeb": f"whatweb {DOMAIN}",
            "Curl": f"curl -I https://{DOMAIN}",
            "Dig": f"dig {DOMAIN}",
            "Traceroute": f"traceroute -w 1 {DOMAIN}",
            "SSLScan": f"sslscan {DOMAIN}"
        }

        results = {}

        for tool_name, command in tools.items():
            execution_time = self.measure_execution_time(command, timeout=10)
            results[tool_name] = {"execution_time": execution_time}
            print(f"{tool_name}: Time={execution_time:.2f}s")

        # Save results
        ensure_reports_directory()
        with open("reports/tools_performance.txt", "w") as f:
            f.write("Other Tools Performance Results\n")
            for tool, data in results.items():
                f.write(f"{tool}: Execution Time: {data['execution_time']:.2f}s\n")

        print("✅ Other tools performance results saved.")

if __name__ == "__main__":
    unittest.main()

