import sys
from contextlib import contextmanager
import time

# ANSI escape codes for colors
CYAN = '\033[96m'
MAGENTA = '\033[95m'
BOLD = '\033[1m'
RESET = '\033[0m'

# rich imports for spinner and progress bar
try:
    from rich.console import Console
    from rich.progress import Progress
    console = Console()
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


def print_ls_for_llm(stdout: str) -> str:
    """ prints the ls command formatted for the LLM """
    entries = [line for line in stdout.strip().splitlines() if line]
    if not entries:
        return "No files or directories found."
    entries.sort()
    lines = ["Directory listing:", "```bash"]
    lines += entries
    lines.append("```")
    return "\n".join(lines)

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

def print_error_output(stderr: str):
    """ Prints the stderr of the subprocess call result """
    if stderr.strip():
        print(f"\n\033[91m[ERROR]{RESET} {stderr}\n" + ("-" * 60) + "\n", file=sys.stderr)

def print_llm_response(response: str):
    """Prints the output of the LLM in magenta with spacing."""
    print(f"\n{MAGENTA}{BOLD}[LLM]:{RESET} {MAGENTA}{response}{RESET}\n")
    print("\n" + ("=" * 60) + "\n")  # Divider line after LLM response

@contextmanager
def spinner(message: str = "Working..."):
    """Context manager for an animated spinner using rich, or fallback."""
    if RICH_AVAILABLE:
        with console.status(f"[bold cyan]{message}", spinner="dots"):
            yield
    else:
        # Simple fallback spinner
        print(message + " ...", end="", flush=True)
        try:
            yield
        finally:
            print(" done.")

def show_progress(total: int, description: str = "Processing"):
    """Show a progress bar using rich, or fallback to text."""
    if RICH_AVAILABLE:
        return Progress(
            "[progress.description]{task.description}",
            "[progress.percentage]{task.percentage:>3.0f}%",
            "{task.completed}/{task.total}",
            console=console
        ).__enter__()
    else:
        # Fallback: simple text progress
        class DummyProgress:
            def add_task(self, description, total):
                print(f"{description} (0/{total})")
                return 1
            def update(self, task, advance=1):
                print(f"Progress: +{advance}")
            def stop(self):
                print("Progress complete.")
        return DummyProgress()
