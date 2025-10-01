import time
import json
import pandas as pd
from utils.app_launcher import open_app, load_apps
from utils.web_search import duckduckgo_search
from nlp.ollama_engine import call_local_llm, retrieve_memory

# Load available apps
apps = load_apps()

# Test prompts
test_prompts = [
    "open calculator",
    "launch vs code",
    "what is today's date?",
    "who is the prime minister of India?",
    "start chrome",
    "tell me a joke"
]

# Models to compare
models = ["llama3.2", "mistral"]

def run_prompt_with_tools(model, prompt):
    """Run a prompt with tool execution pipeline"""
    rag_context = retrieve_memory(prompt, n_results=5)

    # Step 1: Ask LLM for structured decision
    decision_prompt = f"""
    You are HEX AI, an autonomous assistant.
    User asked: {prompt}
    Memory: {rag_context}

    Decide internally:
    - action: 'answer', 'web_search', or 'launch_app'
    - query: if web_search
    - app_name: if launch_app (friendly name)

    Output ONLY JSON like this:
    {{"action": "...", "query": "...", "app_name": "...", "answer": "..."}} 
    """
    llm_response = call_local_llm(decision_prompt, model=model)

    try:
        decision = json.loads(llm_response)
    except Exception:
        return {"final_answer": llm_response, "decision": "parse_error"}

    action = decision.get("action", "answer")
    final_answer = decision.get("answer", "")

    # Step 2: Perform tool actions
    if action == "web_search":
        query = decision.get("query", prompt)
        web_results = duckduckgo_search(query)
        final_answer = call_local_llm(f"""
        User asked: {prompt}
        Web Results: {web_results}
        Memory: {rag_context}

        Give a concise helpful answer.
        """, model=model)

    elif action == "launch_app":
        friendly_name = decision.get("app_name", "").lower()
        # Try to resolve app
        if friendly_name in apps:
            success = open_app(friendly_name)
            if success:
                final_answer = f"✅ Successfully opened {friendly_name}."
            else:
                final_answer = f"❌ Failed to open {friendly_name}."
        else:
            final_answer = f"❌ App '{friendly_name}' not found in available apps."

    return {"final_answer": final_answer, "decision": decision}

def run_benchmark():
    results = []
    for model in models:
        print(f"\n🔍 Testing model: {model}")
        for prompt in test_prompts:
            start = time.time()
            result = run_prompt_with_tools(model, prompt)
            elapsed = round(time.time() - start, 2)

            results.append({
                "model": model,
                "prompt": prompt,
                "decision": result.get("decision"),
                "answer": result.get("final_answer"),
                "time_sec": elapsed
            })

            print(f"📝 {prompt} -> {result.get('final_answer')} ({elapsed:.2f}s)")
    return results

if __name__ == "__main__":
    benchmark_results = run_benchmark()
    df = pd.DataFrame(benchmark_results)
    print("\n📊 Benchmark Summary:")
    print(df[["model", "prompt", "time_sec", "answer"]])
    df.to_csv("benchmark_results.csv", index=False)
