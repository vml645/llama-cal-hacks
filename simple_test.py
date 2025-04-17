from llama_stack_client import LlamaStackClient

client = LlamaStackClient()

response = client.chat.completions.create(
    model="llama3.2:3b",
    messages=[
        {"role": "user", "content": "Who won the 2022 World Cup?"}
    ]
)

print(response.choices[0].message.content)
