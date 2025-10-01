import psutil
import datetime
import os
import csv

log_path = "logs/system_info.csv"
if not os.path.exists("logs"):
    os.makedirs("logs")

def get_system_status():
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    running_apps = []
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name']:
                running_apps.append(proc.info['name'])
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return {
        "timestamp": timestamp,
        "cpu_percent": cpu_percent,
        "memory_percent": memory.percent,
        "running_apps": list(set(running_apps))  # Remove duplicates
    }

def log_system_status():
    data = get_system_status()

    # Write header if needed
    if not os.path.exists(log_path):
        with open(log_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "CPU (%)", "Memory (%)", "Running Apps"])

    # Append current system info
    with open(log_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([data["timestamp"], data["cpu_percent"], data["memory_percent"], "; ".join(data["running_apps"])])

    print(f"📊 Logged system info at {data['timestamp']}")
    return data
