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

    def is_tool_installed(self, tool_name):
        """Check if a tool is installed"""
        return subprocess.call(f"which {tool_name}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0

    def measure_execution_time(self, command):
        """Run a command and measure execution time"""
        start_time = time.time()
        try:
            subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Error executing: {command}, {e}")
        return time.time() - start_time

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
            if not self.is_tool_installed(tool_name.lower().split()[0]):
                print(f"❌ {tool_name} is not installed. Skipping...")
                continue  # ✅ Skip missing tools

            print(f"\n🚀 Running {tool_name}...")
            execution_time = self.measure_execution_time(command)

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
        plt.bar(tool_names, execution_times, color=['blue', 'red', 'green', 'orange', 'purple'])
        plt.ylabel("Time (seconds)")
        plt.title("Execution Time Comparison")
        plt.xticks(rotation=30)
        plt.savefig("reports/execution_time.png")  # ✅ Save graph automatically
        plt.close()

        print("✅ Graphs generated and saved to 'reports/' folder.")

if __name__ == "__main__":
    unittest.main()

