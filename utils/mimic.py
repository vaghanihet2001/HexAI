from pynput import mouse, keyboard
import pyautogui
import time
import json

recorded_actions = []
start_time = None

# ---------- Recording ----------
def record_event(event_type, details):
    global start_time
    if start_time is None:
        start_time = time.time()
    timestamp = time.time() - start_time
    recorded_actions.append({"time": timestamp, "type": event_type, "details": details})

def on_click(x, y, button, pressed):
    record_event("mouse_click", {"x": x, "y": y, "button": str(button), "pressed": pressed})

def on_move(x, y):
    record_event("mouse_move", {"x": x, "y": y})

def on_scroll(x, y, dx, dy):
    record_event("mouse_scroll", {"x": x, "y": y, "dx": dx, "dy": dy})

def on_press(key):
    try:
        record_event("key_press", {"key": key.char})
    except AttributeError:
        record_event("key_press", {"key": str(key)})

def on_release(key):
    record_event("key_release", {"key": str(key)})
    if key == keyboard.Key.esc:  # Stop recording with ESC
        return False

def start_recording():
    with mouse.Listener(on_click=on_click, on_move=on_move, on_scroll=on_scroll) as ml, \
         keyboard.Listener(on_press=on_press, on_release=on_release) as kl:
        ml.join()
        kl.join()
    # Save to file
    with open("recording.json", "w") as f:
        json.dump(recorded_actions, f, indent=2)
    print("🎥 Recording saved!")

# ---------- Playback ----------
def replay():
    with open("recording.json", "r") as f:
        actions = json.load(f)
    start = time.time()
    for action in actions:
        wait_time = action["time"] - (time.time() - start)
        if wait_time > 0:
            time.sleep(wait_time)
        if action["type"] == "mouse_move":
            pyautogui.moveTo(action["details"]["x"], action["details"]["y"])
        elif action["type"] == "mouse_click":
            if action["details"]["pressed"]:
                pyautogui.mouseDown(action["details"]["x"], action["details"]["y"])
            else:
                pyautogui.mouseUp(action["details"]["x"], action["details"]["y"])
        elif action["type"] == "mouse_scroll":
            pyautogui.scroll(action["details"]["dy"])
        elif action["type"] == "key_press":
            pyautogui.keyDown(action["details"]["key"])
        elif action["type"] == "key_release":
            pyautogui.keyUp(action["details"]["key"])

if __name__ == "__main__":
    choice = input("Press R to record, P to play: ").lower()
    if choice == "r":
        start_recording()
    elif choice == "p":
        replay()
