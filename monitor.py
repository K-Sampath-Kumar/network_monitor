import socket
import time
import requests

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from colorama import Fore, Style, init

init()
failure_count = {}

# Load websites from file
def load_websites():
    with open("site.txt", "r") as file:
        websites = [line.strip() for line in file if line.strip()]
    return websites

# DNS check
def check_dns(site):
    try:
        socket.gethostbyname(site)
        return True
    except socket.gaierror:
        return False

# Logging
def log_result(site, status):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("network_log.txt", "a") as log_file:
        log_file.write(f"{timestamp} {site} {status}\n")

# Website check
def check_website(site):
    if not check_dns(site):
        print(Fore.YELLOW + f"Checking {site} : DNS FAILED" + Style.RESET_ALL)
        log_result(site, "DNS FAILED")
        return "DOWN"
    headers = {"User-Agent": "Mozilla/5.0"}
    max_attempts = 3
    success = False
    status_code = None
    latency = None
    for _ in range(max_attempts):
        try:
            start_time = time.time()
            try:
                response = requests.get(f"https://{site}", headers=headers, timeout=5)
            except:
                response = requests.get(f"http://{site}", headers=headers, timeout=5)
            latency = (time.time() - start_time) * 1000  # ms
            status_code = response.status_code
            if status_code < 500:
                success = True
                break
        except requests.RequestException:
            continue
    if success:
        status = "UP"
        print(Fore.GREEN + f"Checking {site} : UP (HTTP {status_code}, {latency:.2f} ms)" + Style.RESET_ALL)
    else:
        status = "DOWN"
        print(Fore.RED + f"Checking {site} : DOWN (HTTP failed)"  + Style.RESET_ALL)
    log_result(site, status)
    return status

# Monitoring
def run_monitoring():
    websites = load_websites()
    up_count = 0
    down_count = 0
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(check_website, websites))
    for site, result in zip(websites, results):
        if result == "DOWN":
            failure_count[site] = failure_count.get(site, 0) + 1
        else:
            failure_count[site] = 0
        if failure_count[site] >= 3:
            print(Fore.RED + f"ALERT: {site} failed 3 times consecutively!" + Style.RESET_ALL)
        if result == "UP":
            up_count += 1
        else:
            down_count += 1
    print("\nSummary Report")
    print("-------------------")
    print("Total websites checked:", len(websites))
    print("UP:", up_count)
    print("DOWN:", down_count)

# Main loop
try:
    while True:
        run_monitoring()
        print("\nWaiting for next check...\n")
        time.sleep(10)
except KeyboardInterrupt:
    print("\nMonitoring stopped by user.")