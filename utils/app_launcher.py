import os
import sys
import json
import subprocess
import platform

LINUX_APP_PATH = r"data/linux_app_path.json"
WINDOWS_APP_PATH = r"data/windows_app_path.json"


def get_app_store_path(system_os=None):
    if not system_os:
        system_os = platform.system()
    return WINDOWS_APP_PATH if system_os == "Windows" else LINUX_APP_PATH


def load_apps(system_os=None):
    path = get_app_store_path(system_os)
    if not os.path.exists(path):
        print(f"⚠️ No apps.json found at {path}")
        return {}
    with open(path, "r") as f:
        return json.load(f)


def save_apps(apps, system_os=None):
    path = get_app_store_path(system_os)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(apps, f, indent=4)


def open_app(app_name):
    system_os = platform.system()
    apps = load_apps(system_os)
    print(apps)
    if app_name not in apps.keys():
        print(f"❌ '{app_name}' not found in saved apps.")
        print(f"➡️ Add it manually: python app_launcher.py add {app_name} <full_path_or_command>")
        return False

    app_entry = apps[app_name]
    exe_path = app_entry["path"]

    try:
        subprocess.Popen([exe_path], shell=True)
        print(f"🚀 Launching '{app_name}' ({app_entry['app_type']}) → {exe_path}")
        return True
    except Exception as e:
        print(f"❌ Error launching '{app_name}': {e}")
        return False


def add_app(app_name, app_path):
    system_os = platform.system()
    apps = load_apps(system_os)
    apps[app_name] = {"path": app_path, "app_type": "custom"}
    save_apps(apps, system_os)
    print(f"✅ Added '{app_name}' -> {app_path}")


def remove_app(app_name):
    system_os = platform.system()
    apps = load_apps(system_os)
    if app_name in apps:
        del apps[app_name]
        save_apps(apps, system_os)
        print(f"🗑️ Removed '{app_name}'")
    else:
        print(f"❌ '{app_name}' not found in apps.json")


def list_apps():
    system_os = platform.system()
    apps = load_apps(system_os)
    if not apps:
        print("📭 No apps saved yet.")
        return
    print("📚 Available Applications:")
    for name, details in apps.items():
        print(f"🔹 {name} ({details['app_type']}) -> {details['path']}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  open <app_name>         → open an app")
        print("  add <name> <path>       → manually add an app")
        print("  remove <app_name>       → remove an app")
        print("  list                    → list saved apps")
        sys.exit(0)

    command = sys.argv[1].lower()

    if command == "open" and len(sys.argv) >= 3:
        open_app(sys.argv[2])
    elif command == "add" and len(sys.argv) >= 4:
        add_app(sys.argv[2], sys.argv[3])
    elif command == "remove" and len(sys.argv) >= 3:
        remove_app(sys.argv[2])
    elif command == "list":
        list_apps()
    else:
        print("❌ Invalid command or missing arguments.")
