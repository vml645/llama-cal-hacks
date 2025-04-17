from printers import print_command, print_command_output, print_error_output
import subprocess
import os
import shlex

current_dir = os.getcwd()

def call_terminal(command: str) -> str:
    """
    Calls the terminal and returns the output. Also prints the command and output to the console.
    Supports `cd` (and `cd ..`) by updating `current_dir`.
    :param command: the specific command to be run in the terminal
    """
    global current_dir
    print_command(command)

    # Split the command so we can intercept cd
    parts = shlex.split(command)
    if parts and parts[0] == "cd":
        # default to home if no path given
        target = parts[1] if len(parts) > 1 else os.path.expanduser("~")
        new_dir = os.path.normpath(os.path.join(current_dir, target))
        if os.path.isdir(new_dir):
            current_dir = new_dir
            return ""  # no output for successful cd
        else:
            err = f"No such directory: {new_dir}"
            print_error_output(err)
            return err

    # For any other command, run in the current_dir
    result = subprocess.run(
        command,
        cwd=current_dir,
        shell=True,
        capture_output=True,
        text=True,
        check=False
    )

    # If there’s stderr, treat it as the “output”
    if result.stderr:
        err = result.stderr.strip()
        print_error_output(err)
        return err

    output = result.stdout.strip()
    print_command_output(output)
    return output
