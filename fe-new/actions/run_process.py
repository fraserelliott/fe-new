from actions.base import Action, ActionPhase, ActionResult
from setup_context import SetupContext
from utils.path_utils import resolve_path
from typing import Optional, Sequence
import subprocess
import shutil
import shlex

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
    def __init__(self, command: Sequence[str], phase: ActionPhase, working_directory: Optional[str] = None, use_parent_dir: bool = False) -> None:
        super().__init__(phase)
        if isinstance(command, str):
            raise ValueError("Command must be a sequence of strings, not a single string")
        if not command:
            raise ValueError("Command cannot be empty")
        self.command = list(command)
        self.working_directory = working_directory
        self.use_parent_dir = use_parent_dir

    def execute(self, context: SetupContext) -> ActionResult:
        working_dir = None
        try:
            print(f"Running process {shlex.join(self.command)}")
            root_dir = context.parent_dir if self.use_parent_dir else context.project_dir
            working_dir = resolve_path(self.working_directory or "", root_dir)
            executable = shutil.which(self.command[0]) or self.command[0]
            command = [executable, *self.command[1:]]
            result = subprocess.run(command, cwd=working_dir)
            if result.returncode == 0:
                return ActionResult(True)
            return ActionResult(False, f"{self.__class__.__name__} failed for '{shlex.join(self.command)}': exit code {result.returncode}")

        except (ValueError, OSError) as e:
            return ActionResult(False, f"{self.__class__.__name__} failed for '{shlex.join(self.command)}' executing at {working_dir}: {e}")
        
class ScaffoldAction(ProcessAction):
    def __init__(self, command: Sequence[str], working_directory: Optional[str] = None, use_parent_dir: bool = False) -> None:
        super().__init__(command, ActionPhase.SCAFFOLD, working_directory, use_parent_dir)

class InstallAction(ProcessAction):
    def __init__(self, command: Sequence[str], working_directory: Optional[str] = None, use_parent_dir: bool = False) -> None:
        super().__init__(command, ActionPhase.INSTALL, working_directory, use_parent_dir)