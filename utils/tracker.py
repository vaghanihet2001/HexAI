import time
import csv
import os
import datetime
import pyautogui
import subprocess
import platform

# Paths
report_path = "logs/daily_report.csv"
screenshot_dir = "logs/screenshots"

if not os.path.exists("logs"):
    os.makedirs("logs")
if not os.path.exists(screenshot_dir):
    os.makedirs(screenshot_dir)

# Detect OS
system_os = platform.system().lower()

def get_active_window():
    try:
        if "windows" in system_os:
            import pygetwindow as gw
            win = gw.getActiveWindow()
            if win:
                return win.title
        elif "linux" in system_os:
            output = subprocess.check_output(
                ["xdotool", "getactivewindow", "getwindowname"],
                stderr=subprocess.DEVNULL
            )
            return output.decode("utf-8").strip()
        else:
            return None
    except Exception:
        return None

def take_screenshot(app_name):
    timestamp = datetime.datetime.now().strftime("%H-%M-%S")
    filename = f"{app_name}_{timestamp}.png".replace(" ", "_").replace("|", "")
    filepath = os.path.join(screenshot_dir, filename)
    screenshot = pyautogui.screenshot()
    screenshot.save(filepath)
    return filepath

def write_log(app, start, end, duration, screenshot_path):
    with open(report_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([app, start, end, f"{duration:.2f}", screenshot_path])

def start_tracking():
    print(f"🕵️ Assistant is now tracking your app usage... ({system_os})")
    current_app = None
    start_time = None

    # Write header if file doesn't exist
    if not os.path.exists(report_path):
        with open(report_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Application", "Start Time", "End Time", "Duration (s)", "Screenshot"])

    try:
        while True:
            active_app = get_active_window()

            if active_app != current_app and active_app is not None:
                now = datetime.datetime.now().strftime("%H:%M:%S")

                # Save data for previous app
                if current_app and start_time:
                    end_time = time.time()
                    duration = end_time - start_time
                    screenshot_path = take_screenshot(current_app)
                    write_log(current_app, start_str, now, duration, screenshot_path)

                # Start tracking new app
                current_app = active_app
                start_time = time.time()
                start_str = now
                print(f"🟢 Switched to: {current_app}")

            time.sleep(1)

    except KeyboardInterrupt:
        print("\n⏹️ Tracking stopped by user.")

if __name__ == "__main__":
    start_tracking()
