from ollama import ChatResponse, chat


"""
Very simple script, calling llama model with a fixed prompt.
Then, it prints the answer.
For demo only.
"""

response: ChatResponse = chat(
    model="gemma3:4b",
    messages=[
        {
            "role": "user",
            "content": "Why is the sky blue?",
        },
    ],
)
print(response.message.content)
