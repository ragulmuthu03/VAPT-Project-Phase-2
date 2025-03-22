import unittest
import os
import time
import psutil
import matplotlib.pyplot as plt

class TestPerformance(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Ensure 'reports' directory exists before running tests."""
        os.makedirs("reports", exist_ok=True)

    def monitor_performance(self, duration=30):
        """Monitor CPU, Memory, and Execution Time while VAPT runs manually."""
        print("\n[+] Start your VAPT tool manually using: sudo python3 tidconsole.py")
        input("[+] Perform all operations and exit the tool. Then press ENTER to continue...")

        start_time = time.time()
        cpu_usages, mem_usages = [], []

        print("[+] Monitoring system performance...")
        while time.time() - start_time < duration:
            cpu_usages.append(psutil.cpu_percent(interval=1))
            mem_usages.append(psutil.virtual_memory().used / (1024 * 1024))  # Convert bytes to MB

        exec_time = time.time() - start_time

        avg_cpu = sum(cpu_usages) / len(cpu_usages)
        avg_mem = sum(mem_usages) / len(mem_usages)

        results = {
            "Execution Time": exec_time,
            "CPU Usage": avg_cpu,
            "Memory Usage": avg_mem
        }

        self.save_results_and_generate_graphs(results, "vapt_performance.txt")

    def compare_other_tools(self):
        """Compare VAPT with other tools."""
        tools = {
            "Nmap": "nmap -sn example.com",
            "Subnet Enumeration": "ipcalc example.com",
            "GeoIP Lookup": "geoiplookup example.com",
            "Traceroute": "traceroute -w 1 example.com",
        }

        results = {"Execution Time": {}, "CPU Usage": {}, "Memory Usage": {}}

        for tool, command in tools.items():
            start_time = time.time()
            try:
                process = os.popen(command)
                process.read()
            except Exception:
                exec_time = 30  # Timeout fallback
            else:
                exec_time = time.time() - start_time

            results["Execution Time"][tool] = exec_time
            results["CPU Usage"][tool] = psutil.cpu_percent(interval=1)
            results["Memory Usage"][tool] = psutil.virtual_memory().used / (1024 * 1024)

        self.save_results_and_generate_graphs(results, "tools_performance.txt")

    def save_results_and_generate_graphs(self, results, file_name):
        """Save results and generate graphs for comparison."""
        file_path = f"reports/{file_name}"
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
        """Monitor and log performance while VAPT is running manually."""
        self.monitor_performance()

    def test_other_tools_performance(self):
        """Compare VAPT results with other tools."""
        self.compare_other_tools()

if __name__ == "__main__":
    unittest.main()

