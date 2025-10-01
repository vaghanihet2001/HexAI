from gpt4all import GPT4All

model_path = r"D:/FunProjects/assistent/models"
# Initialize GPT4All with the local model
llm = GPT4All(
    model_name="Llama-3.2-3B-Instruct-Q4_0",  # Just a label (can be anything)
    model_path=model_path,
    allow_download=False  # Prevent it from trying to download anything
)
def get_llm_response(prompt):
    with llm.chat_session():
        response = llm.generate(prompt)
    return response
