import ollama
response = ollama.chat(
    model="llama3.2:3b",
    messages=[
        {
        "role":"user",
        "content":"definition of ai in 2 lines and name only 3 main type of ai in bullet points"
        }
    ]
)
print(response["message"]["content"])