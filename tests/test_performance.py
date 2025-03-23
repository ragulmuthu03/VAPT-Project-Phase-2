import unittest
import os
import time
import psutil
import subprocess
import matplotlib.pyplot as plt

REPORTS_DIR = "reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

class TestPerformance(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Ensure 'reports' directory exists before running tests."""
        os.makedirs(REPORTS_DIR, exist_ok=True)

    def run_command(self, command):
        """Runs a shell command and measures execution time, CPU, and memory usage."""
        start_time = time.time()

        try:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ps_proc = psutil.Process(process.pid)
            time.sleep(0.1)

            cpu_usage = ps_proc.cpu_percent(interval=0.1)
            memory_usage = ps_proc.memory_info().rss / (1024 * 1024)  # Convert bytes to MB

            process.wait()
            execution_time = time.time() - start_time

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            execution_time, cpu_usage, memory_usage = 30.0, 0.0, 0.0  # Fallback in case of error

        return execution_time, cpu_usage, memory_usage

    def test_vapt_performance(self):
        """Run the VAPT tool and record performance metrics."""
        print("\n[+] Running VAPT performance test...")
        execution_time, cpu_usage, memory_usage = self.run_command("python3 tidconsole.py --test")

        results = {
            "VAPT": {"time": execution_time, "cpu": cpu_usage, "memory": memory_usage}
        }

        self.save_results(results, "vapt_performance.txt")
        self.generate_graphs(results, "VAPT Performance")

    def test_other_tools_performance(self):
        """Compare VAPT performance with other security tools."""
        tools = {
            "Nmap": "nmap -sn example.com",
            "WhatWeb": "whatweb example.com",
            "Curl": "curl -s example.com",
            "Dig": "dig example.com",
            "Traceroute": "traceroute -w 1 example.com",
            "SSLScan": "sslscan example.com",
            "theHarvester": "theHarvester -d example.com -b google"
        }

        results = {}
        for tool, command in tools.items():
            print(f"[+] Running {tool}...")
            execution_time, cpu_usage, memory_usage = self.run_command(command)
            results[tool] = {"time": execution_time, "cpu": cpu_usage, "memory": memory_usage}

        self.save_results(results, "tools_performance.txt")
        self.generate_graphs(results, "Comparison of Security Tools")

    def save_results(self, results, file_name):
        """Save performance results to a file."""
        file_path = os.path.join(REPORTS_DIR, file_name)
        with open(file_path, "w") as f:
            f.write("Tool, Execution Time (s), CPU Usage (%), Memory Usage (MB)\n")
            for tool, data in results.items():
                f.write(f"{tool}, {data['time']:.2f}, {data['cpu']:.2f}, {data['memory']:.2f}\n")

        print(f"✅ Performance results saved to {file_path}")

    def generate_graphs(self, results, title):
        """Generate bar charts for performance metrics."""
        for metric in ["time", "cpu", "memory"]:
            plt.figure(figsize=(10, 6))
            plt.bar(results.keys(), [data[metric] for data in results.values()], color=['blue', 'red', 'green', 'orange', 'purple', 'brown', 'gray'])
            plt.ylabel(metric.capitalize())
            plt.title(f"{title}: {metric.capitalize()} Comparison")
            plt.xticks(rotation=30)
            plt.savefig(f"{REPORTS_DIR}/{metric}_usage.png")
            plt.close()

            print(f"✅ Graph saved as '{REPORTS_DIR}/{metric}_usage.png'")

if __name__ == "__main__":
    unittest.main()

