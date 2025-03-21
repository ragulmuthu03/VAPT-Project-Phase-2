import unittest
import os
import time
import psutil
import subprocess
import matplotlib.pyplot as plt
from memory_profiler import memory_usage

DOMAIN = "example.com"  # ✅ Set target domain

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

    def test_vapt_vs_other_tools(self):
        """Compare VAPT Tool Against Security Tools Based on Loaded Modules"""

        # ✅ Detect which module is loaded (Simulated Input)
        selected_module = "nmap"  # Change this to test different modules (e.g., 'webarchive', 'getgeoip', etc.)

        # ✅ Define tools for comparison based on the selected module
        module_tool_mapping = {
            "nmap": ["Nmap", "WhatWeb", "SSLScan"],
            "webarchive": ["theHarvester", "Curl", "Dig"],
            "getgeoip": ["Curl", "Traceroute"],
            "dnscheck": ["Dig", "WhatWeb"],
        }

        comparison_tools = module_tool_mapping.get(selected_module, ["Nmap", "WhatWeb", "Curl"])  # Default comparison

        tools = {
            "VAPT": {
                "command": f"python3 tidconsole.py",
                "input": f"help\nload scan.{selected_module}\nset TARGET {DOMAIN}\nattack\nexit\n"  # ✅ Load user module dynamically
            }
        }

        # ✅ Add selected tools for comparison dynamically
        if "Nmap" in comparison_tools:
            tools["Nmap"] = f"nmap -sn {DOMAIN}"
        if "WhatWeb" in comparison_tools:
            tools["WhatWeb"] = f"whatweb {DOMAIN}"
        if "Curl" in comparison_tools:
            tools["Curl"] = f"curl -I https://{DOMAIN}"
        if "SSLScan" in comparison_tools:
            tools["SSLScan"] = f"sslscan {DOMAIN}"
        if "theHarvester" in comparison_tools:
            tools["theHarvester"] = f"theHarvester -d {DOMAIN} -b google"
        if "Traceroute" in comparison_tools:
            tools["Traceroute"] = f"traceroute -w 1 {DOMAIN}"
        if "Dig" in comparison_tools:
            tools["Dig"] = f"dig {DOMAIN}"

        results = {}

        for tool_name, data in tools.items():
            if isinstance(data, dict):  # If VAPT (which requires input)
                command, input_commands = data["command"], data["input"]
                execution_time = self.measure_execution_time(command, input_commands, timeout=20)
            else:  # If regular CLI tools
                execution_time = self.measure_execution_time(data, timeout=10)

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

