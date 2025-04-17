def print_ls_for_llm(stdout: str) -> str:
    """ prints the ls command formatted for the LLM """
    # Split into lines and filter out any empties
    entries = [line for line in stdout.strip().splitlines() if line]
    if not entries:
        return "No files or directories found."

    # Sort alphabetically for consistency
    entries.sort()

    # Build the output lines
    lines = ["Directory listing:", "```bash"]
    lines += entries
    lines.append("```")

    # Join and return as one string
    return "\n".join(lines)

def print_command(command: str):
    """ prints the commands called by the LLM """
    pass

def print_command_output(command_output: str):
    """ prints the output of the command called by the LLM """
    pass

def print_error_output(stderr: str):
    """ Prints the stderr of the subprocess call result """
    pass

def print_llm_response(response: str):
    """ prints the output of the LLM """
    pass
