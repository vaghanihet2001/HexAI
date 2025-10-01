import os
import json
import time
import threading
from datetime import datetime
from plyer import notification

REMINDER_FILE = "data/reminders.json"
os.makedirs("data", exist_ok=True)


# ------------------- JSON Storage -------------------
def load_reminders():
    if not os.path.exists(REMINDER_FILE):
        return []
    with open(REMINDER_FILE, "r") as f:
        return json.load(f)


def save_reminders(reminders):
    with open(REMINDER_FILE, "w") as f:
        json.dump(reminders, f, indent=4)


# ------------------- Reminder Management -------------------
def add_reminder(text, time_str):
    reminders = load_reminders()
    reminders.append({"time": time_str, "text": text})
    save_reminders(reminders)


def delete_reminder(text, time_str):
    reminders = load_reminders()
    reminders = [r for r in reminders if not (r["time"] == time_str and r["text"] == text)]
    save_reminders(reminders)


# ------------------- Notification -------------------
def show_notification(title: str, message: str):
    try:
        notification.notify(
            title=title,
            message=message,
            timeout=10  # seconds
        )
    except Exception as e:
        print(f"❌ Notification failed: {e}")


# ------------------- Reminder Loop -------------------
def reminder_loop():
    while True:
        now = datetime.now().strftime("%H:%M")
        reminders = load_reminders()
        updated = False
        for r in reminders[:]:
            if r["time"] == now:
                show_notification("⏰ Reminder", r["text"])
                print(f"🔔 Reminder Triggered: {r['text']}")
                reminders.remove(r)  # remove after triggering
                updated = True
        if updated:
            save_reminders(reminders)
        time.sleep(30)  # check twice per minute


def start_reminder_service():
    t = threading.Thread(target=reminder_loop, daemon=True)
    t.start()
    print("🟢 Reminder service running in background.")
