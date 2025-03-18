import unittest
import os
import time
import psutil
import subprocess
import matplotlib.pyplot as plt
from memory_profiler import memory_usage
import tidconsole  # Import your VAPT tool

DOMAIN = "example.com"  # ✅ Change this to take user input dynamically

class TestPerformance(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Ensure the 'reports' directory exists before running tests."""
        os.makedirs("reports", exist_ok=True)

    def is_tool_installed(self, tool_name):
        """Check if a tool is installed"""
        return subprocess.call(f"which {tool_name}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0

    def measure_execution_time(self, command, timeout=15):
        """Run a command with a timeout and measure execution time"""
        start_time = time.time()
        try:
            subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, check=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            print(f"⚠️ {command} took too long and was terminated.")
            return timeout  # Set to timeout value to avoid blocking
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Error executing: {command}, {e}")
        return time.time() - start_time

    def test_vapt_vs_other_tools(self):
        """Compare VAPT Tool Against Fast Security Tools"""

        tools = {
            "VAPT": f"python3 tidconsole.py -v {DOMAIN} -l scan.nmap",
            "Nmap": f"nmap -sn {DOMAIN}",  # ✅ Only host discovery (fast)
            "WhatWeb": f"whatweb {DOMAIN}",  # ✅ Fast website fingerprinting
            "Curl": f"curl -I https://{DOMAIN}",  # ✅ Fetch HTTP headers
            "Dig": f"dig {DOMAIN}",  # ✅ DNS lookup
            "Traceroute": f"traceroute {DOMAIN}",  # ✅ Network route tracking
            "SSLScan": f"sslscan {DOMAIN}",  # ✅ Quick SSL/TLS security scan
            "theHarvester": f"theHarvester -d {DOMAIN} -b google"  # ✅ OSINT email harvesting
        }

        results = {}

        for tool_name, command in tools.items():
            if not self.is_tool_installed(tool_name.lower().split()[0]):
                print(f"❌ {tool_name} is not installed. Skipping...")
                continue  # ✅ Skip missing tools

            print(f"\n🚀 Running {tool_name} on {DOMAIN} (max {15}s timeout)...")
            execution_time = self.measure_execution_time(command, timeout=15)  # ⏳ Set timeout

            results[tool_name] = {"execution_time": execution_time}
            print(f"{tool_name}: Time={execution_time:.2f}s")

        # Save and generate graphs
        self.save_results_and_generate_graphs(results)

    def save_results_and_generate_graphs(self, results):
        """Save performance results to a file and generate graphs"""
        results_file = "reports/performance_comparison.txt"
        
        execution_times = []
        tool_names = []

        with open(results_file, "w") as f:
            for tool, data in results.items():
                execution_times.append(data['execution_time'])
                tool_names.append(tool)

                f.write(f"{tool}: Execution Time: {data['execution_time']:.2f}s\n")

        print(f"✅ Performance comparison saved to {results_file}")

        # Generate Execution Time Graph
        plt.figure(figsize=(10, 6))
        plt.bar(tool_names, execution_times, color=['blue', 'red', 'green', 'orange', 'purple', 'cyan', 'yellow', 'pink'])
        plt.ylabel("Time (seconds)")
        plt.title("Execution Time Comparison")
        plt.xticks(rotation=30)
        plt.savefig("reports/execution_time.png")  # ✅ Save graph automatically
        plt.close()

        print("✅ Graphs generated and saved to 'reports/' folder.")

if __name__ == "__main__":
    unittest.main()

