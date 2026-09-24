import ollama
while True:
    question=input("ask the question:")
    if question.lower()=="exit":
        break
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