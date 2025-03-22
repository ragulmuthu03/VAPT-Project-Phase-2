import psutil
import time
import os
import subprocess

# Ensure reports directory exists
REPORTS_DIR = "../reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

# File paths for logging
vapt_output = os.path.join(REPORTS_DIR, "vapt_performance.txt")
comparison_output = os.path.join(REPORTS_DIR, "performance_comparison.txt")

# Time interval for VAPT monitoring
INTERVAL = 3  # Seconds

def find_vapt_process():
    """Find the running VAPT process by looking for 'tidconsole.py'."""
    for process in psutil.process_iter(attrs=['pid', 'name', 'cmdline']):
        try:
            if process.info['cmdline'] and 'tidconsole.py' in ' '.join(process.info['cmdline']):
                return process
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return None  # No active process found

def monitor_vapt():
    """Monitor VAPT performance while it's running."""
    vapt_process = find_vapt_process()
    if not vapt_process:
        print("[-] TIDoS Framework is not running!")
        return

    print(f"[+] Monitoring VAPT (Process ID: {vapt_process.pid})...")

    start_time = time.time()
    
    with open(vapt_output, "w") as file:
        file.write("Tool, Timestamp (s), CPU Usage (%), Memory Usage (MB)\n")

    while vapt_process.is_running():
        timestamp = round(time.time() - start_time, 2)
        try:
            memory_usage = vapt_process.memory_info().rss / (1024 * 1024)  # MB
            cpu_usage = vapt_process.cpu_percent(interval=1.0)  # %
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            break  # Process no longer exists

        log_entry = f"VAPT-GeoIP, {timestamp:.2f}, {cpu_usage:.2f}, {memory_usage:.2f}\n"
        print(log_entry.strip())

        with open(vapt_output, "a") as file:
            file.write(log_entry)

        time.sleep(INTERVAL)  # Wait before next measurement

    print("[+] VAPT monitoring completed!")

def measure_tool_performance(tool_name, command):
    """Run an external tool once and record CPU, memory, execution time."""
    print(f"[+] Running {tool_name}...")

    start_time = time.time()

    try:
        # Start process
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(0.1)  # Allow slight delay for process startup

        # Capture process info
        ps_proc = psutil.Process(process.pid)
        memory_usage = ps_proc.memory_info().rss / (1024 * 1024)  # Convert to MB
        cpu_usage = ps_proc.cpu_percent(interval=0.1)  # Get CPU usage

        process.wait()  # Wait for process to finish
        execution_time = time.time() - start_time
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        memory_usage = 0.0
        cpu_usage = 0.0
        execution_time = 0.0

    log_entry = f"{tool_name}, {execution_time:.2f}, {cpu_usage:.2f}, {memory_usage:.2f}\n"
    print(log_entry.strip())

    with open(comparison_output, "a") as file:
        file.write(log_entry)

def compare_performance():
    """Compare VAPT-GeoIP performance with other tools."""
    print("[+] Comparing VAPT-GeoIP with other GeoIP lookup tools...")

    tools = {
        "geoiplookup": "geoiplookup",
        "ipinfo.io": "curl -s ipinfo.io",
        "whois": "whois 8.8.8.8",
        "dig": "dig google.com"
    }

    with open(comparison_output, "w") as file:
        file.write("Tool, Execution Time (s), CPU Usage (%), Memory Usage (MB)\n")

    # Measure each tool
    for tool, command in tools.items():
        measure_tool_performance(tool, command)

    print("[+] Performance comparison complete! Results saved in reports/performance_comparison.txt")

if __name__ == "__main__":
    monitor_vapt()  # Monitor VAPT first
    compare_performance()  # Compare VAPT with other tools

