import json
from ollama import chat, ChatResponse
from utils.memory import load_memory
from utils.rag_memory import retrieve_memory
from utils.web_search import duckduckgo_search, should_search_web

# -------------------- Chat History --------------------
chat_history = []  # stores all messages in current session

# -------------------- LLM Call ------------------------
def call_local_llm(prompt: str,model = "llama3.2",role = "user") -> str:
    """
    Calls the local Llama model with a given prompt.
    """
    response: ChatResponse = chat(
        model=model,
        messages=[{'role': role, 'content': prompt}]
    )
    print("Prompt sent to LLM:\n", prompt)
    return response.message.content.strip()


# -------------------- Prompt Constructor ----------------
def construct_prompt(user_input: str, rag_context: str, history: list, max_messages: int = 5) -> str:
    """
    Builds a prompt including RAG memory and recent chat history.
    """
    # Take last N message pairs (user+assistant)
    recent_history = history[-max_messages*2:]
    conversation_context = "\n".join(
        [f"{msg['role'].capitalize()}: {msg['content']}" for msg in recent_history]
    )

    prompt = f"""
You are HEX AI, a helpful personal assistant. Use the following context to answer:

Memory + RAG Context:
{rag_context}

Conversation History:
{conversation_context}

User Question:
{user_input}

Answer in a friendly, concise, helpful manner.
"""
    return prompt


# -------------------- Main Functions -------------------
def ask_ollama(user_input: str) -> str:
    """
    Ask HEX with RAG memory + chat history (no web search).
    """
    rag_context = retrieve_memory(user_input, n_results=5)
    prompt = construct_prompt(user_input, rag_context, chat_history)
    response = call_local_llm(prompt)

    # Update chat history
    chat_history.append({"role": "user", "content": user_input})
    chat_history.append({"role": "assistant", "content": response})

    return response


def ask_ollama_with_web(user_input: str) -> str:
    """
    Ask HEX with RAG memory + chat history + web search when needed.
    """
    rag_context = retrieve_memory(user_input, n_results=5)
    
    # Check if web search is required
    if should_search_web(user_input, rag_context):
        web_results = duckduckgo_search(user_input)
        print("Web search results:\n", web_results)
        prompt_context = f"Web Results:\n{web_results}\n\nRAG Context:\n{rag_context}"
    else:
        prompt_context = f"RAG Context:\n{rag_context}"

    # Build full prompt with chat history
    prompt = construct_prompt(user_input, prompt_context, chat_history)
    response = call_local_llm(prompt)

    # Save to history
    chat_history.append({"role": "user", "content": user_input})
    chat_history.append({"role": "assistant", "content": response})

    return response


# -------------------- Quick Test ------------------------
if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        response = ask_ollama_with_web(user_input)
        print("HEX:", response)
