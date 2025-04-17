from printers import print_command, print_command_output, print_error_output
import subprocess

def call_terminal(command: str) -> str:
    """
    Calls the terminal and returns the output. Also prints the command and output to the console
    :param command: the specific command to be ran in the terminal
    """
    print_command(command)

    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
        check=True
    )
    output = result.stdout.strip()

    if result.stderr is not None:
        print_error_output(result.stderr.strip())
        return result.stderr.strip()

    print_command_output(output)
    return output
