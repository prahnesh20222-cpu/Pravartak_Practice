import ollama, time
started = time.time()
response = ollama.chat(
    model='gemma3:4b',  # Or 'tinyllama', 'smollm2:1.7b'
    messages=
[{'role': 'user', 'content': "'i see a codeblock that has the following lines. respo = client.chat.completopns.created(model = 'CANDIATE_MODEL'),messages ={'role': 'system'}, {'role':'user'}. What does CANDIDATE_MODEL mean here?"
  }],
               
)
elapsed = time.time() - started
print(f"time take is {elapsed}")
print(response['message']['content'])
