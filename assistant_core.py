import json
from utils.app_launcher import open_app, load_apps
from utils.web_search import duckduckgo_search
from nlp.ollama_engine import call_local_llm, retrieve_memory

# Load all available apps (dictionary: {"friendly_name": "real_app_command"})
apps = load_apps()

def handle_command(command: str) -> str:
    command = command.strip()

    # 1️⃣ Retrieve RAG memory
    rag_context = retrieve_memory(command, n_results=5)

    # 2️⃣ Ask HEX to decide action internally
    prompt = f"""
You are HEX AI, an autonomous assistant.
User asked: {command}
RAG Context: {rag_context}

Decide internally:
- action: 'answer', 'web_search', or 'launch_app'
- query: if web_search
- app_name: if launch_app (friendly name)
- answer: concise answer if action is 'answer'

**Do NOT show JSON to the user.**  
Output internal JSON like this:
{{"action": "...", "query": "...", "app_name": "...", "answer": "..."}}
"""
    llm_response = call_local_llm(prompt)

    # 3️⃣ Parse internal JSON safely
    try:
        decision = json.loads(llm_response)
    except Exception:
        # fallback: just return raw LLM text
        print("❌ Error parsing LLM response:", llm_response)
        return llm_response

    action = decision.get("action", "answer")
    final_answer = decision.get("answer", "")
    print(action)
    # 4️⃣ Execute the decided action
    if action == "web_search":
        query = decision.get("query", command)
        web_results = duckduckgo_search(query)
        # Feed results back to LLM for final answer
        prompt2 = f"""
User asked: {command}
RAG Context: {rag_context}
Web Results: {web_results}

Answer the user's question concisely using the web results and memory.
"""
        final_answer = call_local_llm(prompt2)

    elif action == "launch_app":
        friendly_name = decision.get("app_name")
        # map friendly name to actual app command
        # real_app_name = apps.get(friendly_name)
        real_app_name = None
        if friendly_name in apps.keys():
            real_app_name = friendly_name

        if real_app_name:
            success = open_app(real_app_name)
            if success:
                final_answer = f"✅ Successfully opened {friendly_name}."
            else:
                final_answer = f"❌ Failed to open {friendly_name}."
        else:
            final_answer = f"❌ App '{friendly_name}' not found in available apps."

    # 5️⃣ If action was 'answer', final_answer is already set
    return final_answer
