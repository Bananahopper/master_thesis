import subprocess


def run_commands(commands: list[str]):
    """
    Run a list of commands.

    Args:
        commands (list[str]): list of commands
    """
    for command in commands:
        subprocess.run(command, shell=True)
