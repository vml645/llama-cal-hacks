import sys
from printers import print_llm_response

from llama_stack_client import Agent, LlamaStackClient
client = LlamaStackClient(base_url="http://localhost:11434")
from terminal_calling import call_terminal

# Create the agent
agent = Agent(
    client,
    model="meta-llama/Llama-3.1-8B",
    instructions="You are a helpful assistant that can use tools to run terminal commands. Assume that the terminal command output is provided to the user.",
    tools=[call_terminal],
)


def main():
    user_input = " ".join(sys.argv[1:])
    session_id = agent.create_session("terminal_sessino")
    response = agent.create_turn(
        messages=[{"role": "user", "content": user_input}],
        session_id=session_id,
    )

    print_llm_response(response.output_message.content)

if __name__ == "__main__":
    main()
