import unittest
import os
import time
import psutil
import subprocess
import argparse
import matplotlib.pyplot as plt
from memory_profiler import memory_usage

DOMAIN = "example.com"  # ✅ Set target domain

class TestPerformance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.makedirs("reports", exist_ok=True)

    def is_tool_installed(self, tool_name):
        return subprocess.call(f"which {tool_name}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0

    def measure_execution_time(self, command, input_commands="", timeout=20):
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
            process.communicate(input=input_commands)
        except subprocess.TimeoutExpired:
            print(f"⚠️ {command} took too long and was terminated.")
            return timeout
        return time.time() - start_time

    def test_vapt_performance(self):
        """Run VAPT tool and record performance metrics."""
        tools = {
            "VAPT": {
                "command": "python3 tidconsole.py",
                "input": "help\nvicadd {}\nlist osint-passive\nload getgeoip\nattack getgeoip\nexit\n".format(DOMAIN)
            }
        }
        results = self.run_tools(tools)
        self.save_results(results, "reports/vapt_performance.txt")

    def test_tools_performance(self):
        """Run standard security tools and record performance metrics."""
        tools = {
            "Nmap": f"nmap -sn {DOMAIN}",
            "WhatWeb": f"whatweb {DOMAIN}",
            "Curl": f"curl -I https://{DOMAIN}",
            "Dig": f"dig {DOMAIN}",
            "Traceroute": f"traceroute -w 1 {DOMAIN}",
            "SSLScan": f"sslscan {DOMAIN}",
            "theHarvester": f"theHarvester -d {DOMAIN} -b google"
        }
        results = self.run_tools(tools)
        self.save_results(results, "reports/tools_performance.txt")

    def run_tools(self, tools):
        """Execute tools and measure execution time."""
        results = {}
        for tool_name, data in tools.items():
            if isinstance(data, dict):  # If VAPT (needs interactive input)
                command, input_commands = data["command"], data["input"]
                execution_time = self.measure_execution_time(command, input_commands, timeout=20)
            else:  # Regular CLI tools
                execution_time = self.measure_execution_time(data, timeout=10)
            results[tool_name] = {"execution_time": execution_time}
            print(f"{tool_name}: Time={execution_time:.2f}s")
        return results

    def save_results(self, results, file_path):
        """Save test results to a file."""
        with open(file_path, "w") as f:
            for tool, data in results.items():
                f.write(f"{tool}: Execution Time: {data['execution_time']:.2f}s\n")
        print(f"✅ Results saved to {file_path}")

    def generate_graphs(self):
        """Generate bar graph for execution times."""
        results_file = "reports/performance_comparison.txt"
        execution_times = []
        tool_names = []

        with open(results_file, "r") as f:
            for line in f:
                tool, time_str = line.split(": Execution Time: ")
                execution_times.append(float(time_str.strip().replace("s", "")))
                tool_names.append(tool)

        plt.figure(figsize=(10, 6))
        plt.bar(tool_names, execution_times, color=['blue', 'red', 'green', 'orange', 'purple', 'cyan', 'yellow'])
        plt.ylabel("Time (seconds)")
        plt.title("Execution Time Comparison")
        plt.xticks(rotation=30)
        plt.savefig("reports/execution_time.png")
        plt.close()
        print("✅ Graph generated and saved to 'reports/' folder.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run performance tests")
    parser.add_argument("--mode", choices=["vapt", "tools", "generate_graphs"], required=True, help="Select test mode")
    args = parser.parse_args()

    test = TestPerformance()
    if args.mode == "vapt":
        test.test_vapt_performance()
    elif args.mode == "tools":
        test.test_tools_performance()
    elif args.mode == "generate_graphs":
        test.generate_graphs()

