import unittest
import os
import time
import psutil
import subprocess
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

    def measure_disk_io(self):
        """Measure disk read/write usage"""
        disk_io_start = psutil.disk_io_counters()
        time.sleep(1)  # Allow time for disk operations
        disk_io_end = psutil.disk_io_counters()
        return {
            "read_bytes": (disk_io_end.read_bytes - disk_io_start.read_bytes) / (1024 * 1024),  # MB
            "write_bytes": (disk_io_end.write_bytes - disk_io_start.write_bytes) / (1024 * 1024),  # MB
        }

    def measure_network_traffic(self):
        """Measure network data sent/received"""
        net_io_start = psutil.net_io_counters()
        time.sleep(1)  # Allow time for network operations
        net_io_end = psutil.net_io_counters()
        return {
            "sent": (net_io_end.bytes_sent - net_io_start.bytes_sent) / (1024 * 1024),  # MB
            "received": (net_io_end.bytes_recv - net_io_start.bytes_recv) / (1024 * 1024),  # MB
        }

    def measure_system_load(self):
        """Measure system load (1-minute average)"""
        return psutil.getloadavg()[0]

    def test_vapt_performance(self):
        """Test VAPT Tool Performance Against Nmap"""
        # ✅ Measure Execution Time
        vapt_time = self.measure_execution_time("python3 tidconsole.py -v example.com -l scan.nmap")
        nmap_time = self.measure_execution_time("nmap example.com")

        # ✅ Measure CPU Usage
        vapt_cpu = self.measure_cpu_usage("python3 tidconsole.py -v example.com -l scan.nmap")
        nmap_cpu = self.measure_cpu_usage("nmap example.com")

        # ✅ Measure Memory Usage
        vapt_memory = self.measure_memory_usage(lambda: tidconsole.main())
        nmap_memory = self.measure_memory_usage(lambda: subprocess.run(["nmap", "example.com"], stdout=subprocess.PIPE, stderr=subprocess.PIPE))

        # ✅ Measure Disk I/O
        vapt_disk_io = self.measure_disk_io()
        nmap_disk_io = self.measure_disk_io()

        # ✅ Measure Network Traffic
        vapt_network = self.measure_network_traffic()
        nmap_network = self.measure_network_traffic()

        # ✅ Measure System Load
        vapt_load = self.measure_system_load()
        nmap_load = self.measure_system_load()

        # ✅ Print results
        print("\n🔹 **VAPT Tool Performance vs Nmap** 🔹")
        print(f"Execution Time: VAPT {vapt_time:.2f}s | Nmap {nmap_time:.2f}s")
        print(f"CPU Usage: VAPT {vapt_cpu:.2f}% | Nmap {nmap_cpu:.2f}%")
        print(f"Memory Usage: VAPT {vapt_memory:.2f}MB | Nmap {nmap_memory:.2f}MB")
        print(f"Disk I/O: VAPT Read {vapt_disk_io['read_bytes']:.2f}MB, Write {vapt_disk_io['write_bytes']:.2f}MB")
        print(f"Network: VAPT Sent {vapt_network['sent']:.2f}MB, Received {vapt_network['received']:.2f}MB")
        print(f"System Load: VAPT {vapt_load:.2f} | Nmap {nmap_load:.2f}")

        # ✅ Save results
        self.save_results("VAPT", vapt_time, vapt_cpu, vapt_memory, vapt_disk_io, vapt_network, vapt_load)
        self.save_results("Nmap", nmap_time, nmap_cpu, nmap_memory, nmap_disk_io, nmap_network, nmap_load)

    def save_results(self, tool_name, execution_time, cpu_usage, memory_usage, disk_io, network, system_load):
        """Save performance results to a file"""
        results_file = "reports/performance_results.txt"
        with open(results_file, "a") as f:
            f.write(f"{tool_name}: Execution Time: {execution_time:.2f}s, CPU: {cpu_usage:.2f}%, Memory: {memory_usage:.2f}MB, ")
            f.write(f"Disk Read: {disk_io['read_bytes']:.2f}MB, Disk Write: {disk_io['write_bytes']:.2f}MB, ")
            f.write(f"Network Sent: {network['sent']:.2f}MB, Network Received: {network['received']:.2f}MB, ")
            f.write(f"System Load: {system_load:.2f}\n")

        print(f"✅ Performance results saved to {results_file}")

if __name__ == "__main__":
    unittest.main()

