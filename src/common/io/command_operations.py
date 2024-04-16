import subprocess
import logging


def run_commands(commands):
    """
    Run a list of commands.

    Args:
        commands (list[str]): list of commands
    """
    for command in commands:
        logging.info(f"Running command from command_operations: {command}")
        subprocess.call(command, shell=True)
