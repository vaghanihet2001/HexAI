| #  | Task                                  | Description                                                                                                      | Feasibility | Approx. Time |
| -- | ------------------------------------- | ---------------------------------------------------------------------------------------------------------------- | ----------- | ------------ |
| 1  | **Linux App Launching**               | Extend `app_launcher.py` to reliably launch Linux apps, support `.desktop` files, CLI apps, and custom paths.    | ✅ Very High | 4–6 hours    |
| 2  | **Windows App Launching (existing)**  | Ensure Windows UWP and `.exe` launching works flawlessly (already partially done).                               | ✅ High      | 2–3 hours    |
| 3  | **System Notifications / Reminders**  | Create `notifications.py` using `notify-send` (Linux) and `win10toast` (Windows). Support scheduled reminders.   | ✅ High      | 3–5 hours    |
| 4  | **Persistent Memory with MongoDB**    | Replace `memory.json` with MongoDB. Store: facts, macros, reminders, app paths, indexed files.                   | ✅ High      | 5–8 hours    |
| 5  | **Command Dispatcher Improvements**   | Update `handle_command` to include new modules: reminders, file search, notifications.                           | ✅ High      | 3–4 hours    |
| 6  | **Local File Search Module**          | Build `file_search.py` to search files/folders on the PC quickly, maybe with caching/indexing.                   | ✅ Medium    | 6–10 hours   |
| 7  | **AI Integration – Ollama**           | Ensure `ollama_engine.py` is modular and fallback-ready. Can query LLM for unknown commands or questions.        | ✅ High      | 2–3 hours    |
| 8  | **Optional: ChatGPT API Integration** | Allow queries requiring real-time web info (e.g., “What time is it?”). Can be separate module for future growth. | ✅ Medium    | 4–6 hours    |
| 9  | **Macro Recording & Playback**        | Refactor recording/playback system to support multi-step macros, persist in MongoDB.                             | ✅ High      | 4–5 hours    |
| 10 | **CLI & Terminal UI**                 | Improve terminal interface with colors, input hints, command history, and logging.                               | ✅ High      | 3–4 hours    |
| 11 | **Logging & Debugging Module**        | Add structured logging for actions, errors, and AI responses. Helps track assistant behavior.                    | ✅ High      | 2–3 hours    |
| 12 | **Testing & Error Handling**          | Test all modules on both Linux and Windows, handle failures gracefully.                                          | ✅ High      | 6–8 hours    |
