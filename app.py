import json
from assistant_core import handle_command

def load_memory():
    try:
        with open("memory.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_memory(data):
    with open("memory.json", "w") as f:
        json.dump(data, f, indent=4)

def main():
    memory = load_memory()
    print("🤖 Hello! What can I help you with today?")


    while True:
        user_input = input("🗨️  Command me (or type 'exit'): ")
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break
        responce = handle_command(user_input)
        print("🤖" ,responce)
if __name__ == "__main__":
    main()