import sys

# ANSI escape codes for colors
CYAN = '\033[96m'
MAGENTA = '\033[95m'
BOLD = '\033[1m'
RESET = '\033[0m'


def print_command(command: str):
    """Prints the commands called by the LLM in a cyan box with spacing."""
    box_width = max(60, len(command) + 6)
    top = f"{CYAN}┌{'─' * (box_width - 2)}┐{RESET}"
    label = f"{CYAN}│{BOLD} LLM WILL RUN  {RESET}{CYAN}{' ' * (box_width - 17)}│{RESET}"
    content = f"{CYAN}│  {command.ljust(box_width - 4)}│{RESET}"
    bottom = f"{CYAN}└{'─' * (box_width - 2)}┘{RESET}"
    print("\n" * 2, end='', file=sys.stderr)  # Extra spacing before
    print(top, file=sys.stderr)
    print(label, file=sys.stderr)
    print(content, file=sys.stderr)
    print(bottom, file=sys.stderr)
    print("\n", file=sys.stderr)  # Extra spacing after


def print_command_output(command_output: str):
    """Prints the output of the command called by the LLM, clearly separated with spacing."""
    print(f"\n{BOLD}[COMMAND OUTPUT]{RESET}")
    print(command_output)
    print("\n" + ("-" * 60) + "\n")  # Divider line after output


def print_llm_response(response: str):
    """Prints the output of the LLM in magenta with spacing."""
    print(f"\n{MAGENTA}{BOLD}[LLM]:{RESET} {MAGENTA}{response}{RESET}\n")
    print("\n" + ("=" * 60) + "\n")  # Divider line after LLM response
