import unittest
import os
import time
import psutil
import subprocess
import matplotlib.pyplot as plt
from memory_profiler import memory_usage

DOMAIN = "example.com"
REPORTS_DIR = "reports"

class TestPerformance(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Ensure 'reports' directory exists before running tests."""
        os.makedirs(REPORTS_DIR, exist_ok=True)

    def measure_metrics(self, command):
        """Run a command, measure execution time, CPU, and memory usage."""
        start_time = time.time()
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        mem_usage = memory_usage(process, interval=0.1)  # Capture memory usage during execution
        process.communicate()  # Wait for process to finish

        exec_time = time.time() - start_time
        cpu_usage = psutil.cpu_percent(interval=1)
        max_memory = max(mem_usage)

        return exec_time, cpu_usage, max_memory

    def test_vapt_performance(self):
        """Measure performance of VAPT tool after user execution."""
        print("\n[+] Run VAPT manually, execute required operations, and then exit.")
        input("Press Enter after completing execution...")  # Wait for user to finish

        exec_time, cpu_usage, mem_usage = self.measure_metrics("sudo python3 tidconsole.py --quiet")

        results = {
            "Execution Time (s)": exec_time,
            "CPU Usage (%)": cpu_usage,
            "Memory Usage (MB)": mem_usage
        }

        self.save_results("vapt_performance.txt", results)
        self.generate_graphs(results, "VAPT Performance")

    def test_other_tools_performance(self):
        """Measure performance of external tools."""
        tools = {
            "Nmap": f"nmap -sn {DOMAIN}",
            "Subnet Enumeration": f"ipcalc {DOMAIN}",
            "GeoIP Lookup": f"geoiplookup {DOMAIN}",
            "Traceroute": f"traceroute -w 1 {DOMAIN}"
        }

        results = {"Execution Time (s)": {}, "CPU Usage (%)": {}, "Memory Usage (MB)": {}}

        for tool, command in tools.items():
            exec_time, cpu_usage, mem_usage = self.measure_metrics(command)
            results["Execution Time (s)"][tool] = exec_time
            results["CPU Usage (%)"][tool] = cpu_usage
            results["Memory Usage (MB)"][tool] = mem_usage
            print(f"{tool}: Time={exec_time:.2f}s, CPU={cpu_usage:.2f}%, Memory={mem_usage:.2f}MB")

        self.save_results("tools_performance.txt", results)
        self.generate_graphs(results, "Comparison with Other Tools")

    def save_results(self, filename, results):
        """Save results to a file."""
        file_path = os.path.join(REPORTS_DIR, filename)
        with open(file_path, "w") as f:
            for metric, data in results.items():
                if isinstance(data, dict):
                    f.write(f"{metric}:\n")
                    for tool, value in data.items():
                        f.write(f"{tool}: {value:.2f}\n")
                else:
                    f.write(f"{metric}: {data:.2f}\n")
            f.write("\n")

        print(f"✅ {file_path} saved.")

    def generate_graphs(self, results, title):
        """Generate graphs for comparison."""
        for metric, data in results.items():
            plt.figure(figsize=(10, 6))
            if isinstance(data, dict):
                plt.bar(data.keys(), data.values(), color=['blue', 'red', 'green', 'orange', 'purple'])
            else:
                plt.bar([title], [data], color='blue')
            plt.ylabel(metric)
            plt.title(f"{metric} - {title}")
            plt.xticks(rotation=30)
            plt.savefig(f"{REPORTS_DIR}/{metric.replace(' ', '_').lower()}.png")
            plt.close()

            print(f"✅ {metric} graph saved as '{REPORTS_DIR}/{metric.replace(' ', '_').lower()}.png'")

if __name__ == "__main__":
    unittest.main()

