import subprocess
import json
import sys
import os
from llama_stack_client import Agent, AgentEventLogger, RAGDocument, LlamaStackClient  # Agent / RAGDocument unused but allowed

# ---------- local helper ---------- #
def terminal_call(command: str) -> str:
    """Run a shell command and return stdout / stderr."""
    print(f"$ {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    output = result.stdout.strip() if result.returncode == 0 else result.stderr.strip()
    print(output)
    return output


# ---------- Llama Stack setup ---------- #
client = LlamaStackClient(base_url="http://localhost:8321")
model_id = next(m for m in client.models.list() if m.model_type == "llm").identifier

# *** VERY IMPORTANT: use tool_name, not name ***
tools = [
    {
        "tool_name": "terminal_call",
        "description": "Execute a shell command on the local machine",
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

# ---------- main routine ---------- #
def main() -> None:
    user_input = " ".join(sys.argv[1:]) or "echo hello world"

    # first pass – ask the model
    messages = [{"role": "user", "content": user_input}]
    first = client.inference.chat_completion(
        model_id=model_id,
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    msg = first.completion_message

    if msg.tool_calls:
        # model asked to run our tool
        for call in msg.tool_calls:
            args = json.loads(call.arguments)
            result = terminal_call(**args)

            # feed result back
            messages.extend([
                {
                    "role": "assistant",
                    "content": None,
                    "function_call": {
                        "name": call.name,
                        "arguments": call.arguments
                    }
                },
                {"role": "tool", "name": call.name, "content": result}
            ])

        follow_up = client.inference.chat_completion(
            model_id=model_id,
            messages=messages
        )
        print(follow_up.completion_message.content)
    else:
        # direct answer
        print(msg.content)


if __name__ == "__main__":
    main()
