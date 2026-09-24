import ollama
response = ollama.chat(
    model="llama3.2:3b",
    messages=[
        {
        "role":"user",
        "content":"what is ai"
        }
    ]
)
print(response["message"]["content"])