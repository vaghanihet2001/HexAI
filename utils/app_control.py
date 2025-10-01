import subprocess
import os
import platform
import time

# Only import pygetwindow and pyautogui if on Windows
if platform.system() == "Windows":
    import pygetwindow as gw
    import pyautogui
else:
    gw = None
    try:
        import pyautogui
    except ImportError:
        pyautogui = None

def open_vscode(vscode_path=None):
    
    system_os = platform.system()
    # If no path provided, try default binary for Linux/Windows
    if not vscode_path:
        if system_os == "Linux":
            vscode_path = "code"
        elif system_os == "Windows":
            vscode_path = os.path.expanduser("~\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe")

    # # Check path existence only for Windows
    # if system_os == "Windows" and (not vscode_path or not os.path.exists(vscode_path)):
    #     print("❌ VS Code path is not set or incorrect.")
    #     return

    try:
        subprocess.Popen([vscode_path])
        print("🟢 VS Code opened.")
    except Exception as e:
        print(f"❌ Error opening VS Code: {e}")
    return


def focus_window(title_keyword):
    system_os = platform.system()
    if system_os != "Windows":
        print("⚠️ focus_window not supported on Linux.")
        return False

    if not gw:
        print("⚠️ pygetwindow not available on this platform.")
        return False

    for window in gw.getWindowsWithTitle(title_keyword):
        window.activate()
        print(f"🪟 Focused: {window.title}")
        return True
    print(f"❌ Could not find window with keyword: {title_keyword}")
    return False


def click_and_type(x, y, text):
    if not pyautogui:
        print("⚠️ pyautogui not available on this platform.")
        return
    pyautogui.click(x, y)
    time.sleep(1)
    pyautogui.typewrite(text)
    print(f"⌨️ Typed: {text}")
