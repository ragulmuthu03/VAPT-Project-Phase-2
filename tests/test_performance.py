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

    def measure_execution_time(self, command, input_commands=""):
        """Run a command with automated user input and measure execution time."""
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
            return 30  # Default timeout if it takes too long
        return time.time() - start_time

    def measure_cpu_memory(self, command, input_commands=""):
        """Measure CPU and memory usage."""
        process = psutil.Process()
        start_cpu = process.cpu_percent(interval=1)
        mem_usage = memory_usage((subprocess.run, (command,), {"shell": True}), interval=0.1)
        return start_cpu, max(mem_usage)

    def run_tool_tests(self, tools, file_name):
        """Run all tools and collect performance metrics."""
        results = {"Execution Time": {}, "CPU Usage": {}, "Memory Usage": {}}

        for tool, data in tools.items():
            if isinstance(data, dict):  # If VAPT (which requires input)
                command, input_commands = data["command"], data["input"]
                exec_time = self.measure_execution_time(command, input_commands)
                cpu_usage, mem_usage = self.measure_cpu_memory(command, input_commands)
            else:  # If regular CLI tools
                exec_time = self.measure_execution_time(data)
                cpu_usage, mem_usage = self.measure_cpu_memory(data)

            results["Execution Time"][tool] = exec_time
            results["CPU Usage"][tool] = cpu_usage
            results["Memory Usage"][tool] = mem_usage

            print(f"{tool}: Time={exec_time:.2f}s, CPU={cpu_usage:.2f}%, Memory={mem_usage:.2f}MB")

        self.save_results_and_generate_graphs(results, file_name)

    def test_vapt_performance(self):
        """Measure VAPT tool performance for selected modules."""
        tools = {
            "VAPT": {
                "command": "sudo python3 tidconsole.py",  # ✅ Run with root privileges
                "input": "help\nload scan.nmap\nset TARGET {}\nattack\nexit\n".format(DOMAIN)
            },
        }
        self.run_tool_tests(tools, "vapt_performance.txt")

    def test_other_tools_performance(self):
        """Measure performance of external tools comparable to VAPT modules."""
        tools = {
            "Nmap": f"nmap -sn {DOMAIN}",
            "Subnet Enumeration": f"ipcalc {DOMAIN}",
            "GeoIP Lookup": f"geoiplookup {DOMAIN}",
        }
        self.run_tool_tests(tools, "tools_performance.txt")

    def save_results_and_generate_graphs(self, results, file_name):
        """Save results and generate graphs for comparison."""
        file_path = f"reports/{file_name}"
        with open(file_path, "w") as f:
            for metric, data in results.items():
                f.write(f"{metric}:\n")
                for tool, value in data.items():
                    f.write(f"{tool}: {value:.2f}\n")
                f.write("\n")

        print(f"✅ {file_path} saved.")

        # Generate separate graphs for Execution Time, CPU Usage, and Memory Usage
        for metric, data in results.items():
            plt.figure(figsize=(10, 6))
            plt.bar(data.keys(), data.values(), color=['blue', 'red', 'green', 'orange', 'purple'])
            plt.ylabel(metric)
            plt.title(f"{metric} Comparison (VAPT vs. Other Tools)")
            plt.xticks(rotation=30)
            plt.savefig(f"reports/{metric.lower().replace(' ', '_')}.png")
            plt.close()

            print(f"✅ {metric} graph saved as 'reports/{metric.lower().replace(' ', '_')}.png'")


if __name__ == "__main__":
    unittest.main()

