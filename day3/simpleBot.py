import ollama
question=input("ask the question:")
response = ollama.chat(
    model="llama3.2:3b",
    messages=[
        {
            "role": "system",
            "content": "give me ans in 2 3 lines."
        },
        {
            "role": "user",
            "content":question
        }
    ]
)
print(response["message"]["content"])