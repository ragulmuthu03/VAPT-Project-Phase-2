import unittest
import os
import time
import psutil
import subprocess
import matplotlib.pyplot as plt
from memory_profiler import memory_usage
import tidconsole  # Import your VAPT tool

class TestPerformance(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Ensure the 'reports' directory exists before running tests."""
        os.makedirs("reports", exist_ok=True)

    def measure_execution_time(self, command):
        """Run a command and measure execution time"""
        start_time = time.time()
        try:
            subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Error executing: {command}, {e}")
        return time.time() - start_time

    def measure_cpu_usage(self, command):
        """Run a command and measure CPU usage"""
        process = psutil.Process()
        start_cpu = process.cpu_percent(interval=1)

        try:
            subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Error executing: {command}, {e}")

        return process.cpu_percent(interval=1) - start_cpu

    def measure_memory_usage(self, function):
        """Run a function and measure memory usage"""
        try:
            mem_usage = memory_usage(function, interval=0.1)
            return max(mem_usage)
        except Exception as e:
            print(f"⚠️ Error measuring memory: {e}")
            return -1

    def test_vapt_vs_other_tools(self):
        """Compare VAPT Tool Against Nmap, Nikto, Wapiti, OpenVAS"""

        tools = {
            "VAPT": "python3 tidconsole.py -v example.com -l scan.nmap",
            "Nmap": "nmap example.com",
            "Nikto": "nikto -h example.com",
            "Wapiti": "wapiti -u http://example.com",
            "OpenVAS": "omp -u admin -w password --xml '<task>OpenVAS Task</task>'"
        }

        results = {}

        for tool_name, command in tools.items():
            print(f"\n🚀 Running {tool_name}...")
            execution_time = self.measure_execution_time(command)
            cpu_usage = self.measure_cpu_usage(command)
            memory_usage = self.measure_memory_usage(lambda: subprocess.run(command, shell=True))

            results[tool_name] = {
                "execution_time": execution_time,
                "cpu_usage": cpu_usage,
                "memory_usage": memory_usage
            }

            print(f"{tool_name}: Time={execution_time:.2f}s, CPU={cpu_usage:.2f}%, Memory={memory_usage:.2f}MB")

        # Save and generate graphs
        self.save_results_and_generate_graphs(results)

    def save_results_and_generate_graphs(self, results):
        """Save performance results to a file and generate graphs"""
        results_file = "reports/performance_comparison.txt"
        
        execution_times = []
        cpu_usages = []
        memory_usages = []
        tool_names = []

        with open(results_file, "w") as f:
            for tool, data in results.items():
                execution_times.append(data['execution_time'])
                cpu_usages.append(data['cpu_usage'])
                memory_usages.append(data['memory_usage'])
                tool_names.append(tool)

                f.write(f"{tool}: Execution Time: {data['execution_time']:.2f}s, CPU: {data['cpu_usage']:.2f}%, Memory: {data['memory_usage']:.2f}MB\n")

        print(f"✅ Performance comparison saved to {results_file}")

        # Generate Graphs
        self.generate_graphs(tool_names, execution_times, cpu_usages, memory_usages)

    def generate_graphs(self, tools, execution_time, cpu_usage, memory_usage):
        """Automatically generate and save graphs"""

        def plot_graph(metric, values, ylabel, title, filename):
            plt.figure(figsize=(10, 6))
            plt.bar(tools, values, color=['blue', 'red', 'green', 'orange', 'purple'])
            plt.ylabel(ylabel)
            plt.title(title)
            plt.xticks(rotation=30)
            plt.savefig(f"reports/{filename}")  # ✅ Save graphs automatically
            plt.close()

        plot_graph("Execution Time", execution_time, "Time (seconds)", "Execution Time Comparison", "execution_time.png")
        plot_graph("CPU Usage", cpu_usage, "CPU Usage (%)", "CPU Usage Comparison", "cpu_usage.png")
        plot_graph("Memory Usage", memory_usage, "Memory Usage (MB)", "Memory Usage Comparison", "memory_usage.png")

        print("✅ Graphs generated and saved to 'reports/' folder.")

if __name__ == "__main__":
    unittest.main()

