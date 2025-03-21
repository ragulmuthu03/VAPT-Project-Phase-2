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
        """Ensure 'reports' directory exists before running tests."""
        os.makedirs("reports", exist_ok=True)

    def measure_execution_time(self, command):
        """Run a command and measure execution time"""
        start_time = time.time()
        try:
            subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Error executing: {command}, {e}")
        return time.time() - start_time

    def measure_cpu_memory_usage(self, function):
        """Run a function and measure CPU and Memory usage"""
        mem_usage = memory_usage(function, interval=0.1)
        process = psutil.Process()
        cpu_usage = process.cpu_percent(interval=1)
        return max(mem_usage), cpu_usage

    def test_vapt_modules(self):
        """Test three VAPT modules separately"""

        vapt_modules = {
            "Nmap Scan": f"sudo python3 tidconsole.py -l scan.nmap -v {DOMAIN}",  # ✅ Run with sudo
            "Subnet Enumeration": f"sudo python3 tidconsole.py -l scan.subnet -v {DOMAIN}",
            "GeoIP Lookup": f"sudo python3 tidconsole.py -l osint-passive.getgeoip -v {DOMAIN}"
        }

        results = {}

        for module, command in vapt_modules.items():
            exec_time = self.measure_execution_time(command)
            mem_usage, cpu_usage = self.measure_cpu_memory_usage(lambda: subprocess.run(command, shell=True))

            results[module] = {
                "execution_time": exec_time,
                "memory_usage": mem_usage,
                "cpu_usage": cpu_usage
            }

            print(f"{module}: Time={exec_time:.2f}s, Memory={mem_usage:.2f}MB, CPU={cpu_usage:.2f}%")

        # Save VAPT results
        self.save_results("vapt_performance.txt", results)

    def test_external_tools(self):
        """Test equivalent external tools"""

        external_tools = {
            "Nmap": f"nmap -sn {DOMAIN}",
            "Subnet Enumeration": f"ipcalc {DOMAIN}",
            "GeoIP Lookup": f"geoiplookup {DOMAIN}"
        }

        results = {}

        for tool, command in external_tools.items():
            exec_time = self.measure_execution_time(command)
            mem_usage, cpu_usage = self.measure_cpu_memory_usage(lambda: subprocess.run(command, shell=True))

            results[tool] = {
                "execution_time": exec_time,
                "memory_usage": mem_usage,
                "cpu_usage": cpu_usage
            }

            print(f"{tool}: Time={exec_time:.2f}s, Memory={mem_usage:.2f}MB, CPU={cpu_usage:.2f}%")

        # Save external tools' results
        self.save_results("tools_performance.txt", results)

    def save_results(self, filename, results):
        """Save performance results to a file"""
        with open(f"reports/{filename}", "w") as f:
            for tool, data in results.items():
                f.write(f"{tool}: Execution Time: {data['execution_time']:.2f}s, "
                        f"Memory: {data['memory_usage']:.2f}MB, CPU: {data['cpu_usage']:.2f}%\n")
        print(f"✅ {filename} saved.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run performance tests for VAPT and external tools.")
    parser.add_argument("--mode", choices=["vapt", "tools"], required=True, help="Select test mode: 'vapt' or 'tools'")
    args = parser.parse_args()

    suite = unittest.TestSuite()
    
    if args.mode == "vapt":
        suite.addTest(TestPerformance("test_vapt_modules"))
    elif args.mode == "tools":
        suite.addTest(TestPerformance("test_external_tools"))

    runner = unittest.TextTestRunner()
    runner.run(suite)

