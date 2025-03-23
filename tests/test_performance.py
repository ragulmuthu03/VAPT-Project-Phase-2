import unittest
import os
import time
import psutil
import subprocess

REPORTS_DIR = "reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

class TestPerformance(unittest.TestCase):
    
    def run_tool(self, command):
        """Run a tool and measure execution time, CPU, and memory usage."""
        start_time = time.time()
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ps_process = psutil.Process(process.pid)
        cpu_usage = ps_process.cpu_percent(interval=0.1)
        memory_usage = ps_process.memory_info().rss / (1024 * 1024)  # Convert to MB
        process.communicate()
        execution_time = time.time() - start_time
        return execution_time, cpu_usage, memory_usage
    
    def test_vapt_performance(self):
        """Measure performance of the VAPT tool."""
        execution_time, cpu_usage, memory_usage = self.run_tool("python3 tidconsole.py --test")
        
        results = f"VAPT: Time={execution_time:.2f}s, CPU={cpu_usage:.2f}%, Memory={memory_usage:.2f}MB\n"
        print(results)
        
        with open(os.path.join(REPORTS_DIR, "vapt_performance.txt"), "w") as file:
            file.write(results)
    
    def test_other_tools_performance(self):
        """Compare VAPT with other common tools."""
        tools = {
            "Nmap": "nmap -sn 127.0.0.1",
            "WhatWeb": "whatweb 127.0.0.1",
            "Curl": "curl -s 127.0.0.1",
            "Dig": "dig google.com",
            "Traceroute": "traceroute 127.0.0.1",
            "SSLScan": "sslscan google.com",
            "theHarvester": "theHarvester -d google.com -l 1 -b google",
        }

        with open(os.path.join(REPORTS_DIR, "performance_comparison.txt"), "w") as file:
            file.write("Tool, Execution Time (s), CPU Usage (%), Memory Usage (MB)\n")
            
            for tool, command in tools.items():
                execution_time, cpu_usage, memory_usage = self.run_tool(command)
                results = f"{tool}, {execution_time:.2f}, {cpu_usage:.2f}, {memory_usage:.2f}\n"
                print(results.strip())
                file.write(results)

if __name__ == "__main__":
    unittest.main()

