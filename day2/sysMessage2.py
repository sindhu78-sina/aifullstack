import ollama
response = ollama.chat(
    model="llama3.2:3b",
    messages=[
        {
            "role": "system",
            "content": "you are teaching a 5 year old kid, give me answer in 2 3 lines only."
        },
        {
            "role": "user",
            "content": "explain ai"
        }
    ]
)
print(response["message"]["content"])