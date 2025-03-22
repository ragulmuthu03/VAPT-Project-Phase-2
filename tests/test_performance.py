import unittest
import os
import time
import psutil
import subprocess
import matplotlib.pyplot as plt
from memory_profiler import memory_usage

DOMAIN = "example.com"

class TestPerformance(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Ensure 'reports' directory exists before running tests."""
        os.makedirs("reports", exist_ok=True)

    def measure_vapt_performance(self):
        """Run VAPT tool manually and measure performance metrics."""
        print("\n[+] Start VAPT manually using: sudo python3 tidconsole.py")
        input("[+] Perform operations in CLI and exit when done. Press Enter to continue...")

        # Measure CPU and Memory usage after execution
        process = psutil.Process(os.getpid())
        cpu_usage = process.cpu_percent(interval=1)
        mem_usage = process.memory_info().rss / (1024 * 1024)  # Convert bytes to MB

        exec_time = time.time() - self.start_time  # Calculate execution duration

        results = {
            "Execution Time": exec_time,
            "CPU Usage": cpu_usage,
            "Memory Usage": mem_usage
        }

        self.save_results_and_generate_graphs(results, "vapt_performance.txt")

    def measure_tools_performance(self):
        """Measure performance of external tools."""
        tools = {
            "Nmap": f"nmap -sn {DOMAIN}",
            "Subnet Enumeration": f"ipcalc {DOMAIN}",
            "GeoIP Lookup": f"geoiplookup {DOMAIN}",
            "Traceroute": f"traceroute -w 1 {DOMAIN}",
        }

        results = {"Execution Time": {}, "CPU Usage": {}, "Memory Usage": {}}

        for tool, command in tools.items():
            start_time = time.time()
            try:
                process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                process.communicate()
            except subprocess.TimeoutExpired:
                exec_time = 30  # Default timeout
            else:
                exec_time = time.time() - start_time

            ps_proc = psutil.Process(os.getpid())
            cpu_usage = ps_proc.cpu_percent(interval=1)
            mem_usage = ps_proc.memory_info().rss / (1024 * 1024)

            results["Execution Time"][tool] = exec_time
            results["CPU Usage"][tool] = cpu_usage
            results["Memory Usage"][tool] = mem_usage

            print(f"{tool}: Time={exec_time:.2f}s, CPU={cpu_usage:.2f}%, Memory={mem_usage:.2f}MB")

        self.save_results_and_generate_graphs(results, "tools_performance.txt")

    def save_results_and_generate_graphs(self, results, file_name):
        """Save results and generate graphs for comparison."""
        file_path = f"reports/{file_name}"
        with open(file_path, "w") as f:
            for metric, data in results.items():
                f.write(f"{metric}:\n")
                if isinstance(data, dict):
                    for tool, value in data.items():
                        f.write(f"{tool}: {value:.2f}\n")
                else:
                    f.write(f"{data:.2f}\n")
                f.write("\n")

        print(f"✅ {file_path} saved.")

        # Generate separate graphs for Execution Time, CPU Usage, and Memory Usage
        for metric, data in results.items():
            plt.figure(figsize=(10, 6))
            plt.bar(data.keys(), data.values(), color=['blue', 'red', 'green', 'orange'])
            plt.ylabel(metric)
            plt.title(f"{metric} Comparison (VAPT vs. Other Tools)")
            plt.xticks(rotation=30)
            plt.savefig(f"reports/{metric.lower().replace(' ', '_')}.png")
            plt.close()

            print(f"✅ {metric} graph saved as 'reports/{metric.lower().replace(' ', '_')}.png'")

    def test_vapt_performance(self):
        """Measure performance of VAPT tool after user execution."""
        self.start_time = time.time()
        self.measure_vapt_performance()

    def test_other_tools_performance(self):
        """Measure performance of external tools."""
        self.measure_tools_performance()

if __name__ == "__main__":
    unittest.main()

