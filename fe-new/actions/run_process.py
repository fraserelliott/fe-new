from actions.base import Action, ActionPhase, ActionResult
from setup_context import SetupContext
from utils.path_utils import resolve_path
from typing import Optional, Sequence
import subprocess

class ProcessAction(Action):
    """
    Executes an external process within the project context.

    The command is executed without a shell and must be provided as a list of
    arguments.

    Rules:
    - The command is executed directly (shell=False).
    - If a working directory is provided:
        - It must resolve within the project root.
        - Otherwise execution fails.
    - If no working directory is provided, the project root is used.
    - Output is streamed directly to the console.
    - If the process exits with code 0, the action succeeds.
    - If the process exits with a non-zero code, the action fails.
    - If the process cannot be started, the action fails.
    - This action does not execute commands outside the project root.

    Returns:
        True if the process completes successfully (exit code 0).
        False if the process fails or cannot be executed.
    """
    def __init__(self, command: Sequence[str], working_directory: Optional[str]) -> None:
        if isinstance(command, str):
            raise ValueError("Command must be a sequence of strings, not a single string")
        if not command:
            raise ValueError("Command cannot be empty")
        self.command = list(command)
        self.working_directory = working_directory

    def execute(self, context: SetupContext) -> ActionResult:
        try:
            working_dir = resolve_path(self.working_directory or "", context.project_path)
            result = subprocess.run(self.command, cwd=working_dir)
            if result.returncode == 0:
                return ActionResult(True)
            return ActionResult(False, f"{self.__class__.__name__} failed for '{self.command}': exit code {result.returncode}")

        except (ValueError, OSError) as e:
            return ActionResult(False, f"{self.__class__.__name__} failed for '{self.command}': {e}")
        
def ScaffoldAction(ProcessAction):
    phase = ActionPhase.SCAFFOLD

def InstallAction(ProcessAction):
    phase = ActionPhase.INSTALL