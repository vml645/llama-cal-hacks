import sys
from printers import print_llm_response

from llama_stack_client import Agent, LlamaStackClient
client = LlamaStackClient(base_url="http://localhost:11434")
from terminal_calling import call_terminal

<<<<<<< HEAD
dotenv.load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY


def terminal_call(command: str) -> str:
    """Run the command in a shell and return its stdout."""
    printers.print_command(command)
    with printers.spinner(f"Running: {command}"):
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )
    output = result.stdout.strip()
    printers.print_command_output(output)
    if result.stderr:
        printers.print_error_output(result.stderr)
    return output


functions = [
    {
        "name": "terminal_call",
        "description": "Execute a shell command",
        "parameters": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The shell command to run"
                }
            },
            "required": ["command"]
        }
    }
]


def main():
    user_input = " ".join(sys.argv[1:]) or "echo hello"

    # 1) first pass: ask the model, let it choose to call terminal_call
    with printers.spinner("LLM thinking..."):
        resp = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": user_input}],
            functions=functions,
            function_call="auto"
        )
    msg = resp.choices[0].message

    # 2) if it wants to call your function:
    if msg.function_call:
        func_name = msg.function_call.name
        args = json.loads(msg.function_call.arguments)
        result = terminal_call(**args)

        # 3) feed the function result back into the model
        with printers.spinner("LLM follow-up..."):
            follow_up = openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "user", "content": user_input},
                    {
                        "role": "assistant",
                        "content": None,
                        "function_call": {
                            "name": func_name,
                            "arguments": msg.function_call.arguments
                        }
                    },
                    {"role": "function", "name": func_name, "content": result}
                ]
            )
        printers.print_llm_response(follow_up.choices[0].message.content)
    else:
        # if it didn’t call the function, just print its reply
        printers.print_llm_response(msg.content)
=======
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
>>>>>>> 2b30808 (added client)

    print_llm_response(response.output_message.content)

if __name__ == "__main__":
    main()
