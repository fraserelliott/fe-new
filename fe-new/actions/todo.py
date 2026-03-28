from actions.base import Action, ActionPhase, ActionResult
from setup_context import SetupContext
from typing import Optional
from utils.path_utils import resolve_path
from utils.file_utils import append_text, safe_write_text_file

class TodoAction(Action):
    """
    Writes actions for the user to take post-setup.

    Rules:
    - Will only write to {project_dir}/SETUP.md
    - Will create the file if it does not exist yet
    - The provided content is appended to the end of the file.

    Returns:
        True if content was successfully written.
        False if the operation fails.
    """
    phase = ActionPhase.UPDATE_FILE

    def __init__(self, content: str) -> None:
        self.content = content
    
    def execute(self, context: SetupContext) -> ActionResult:
        try:
            todo_path = resolve_path("SETUP.md", context.project_dir)
            if not todo_path.is_file():
                safe_write_text_file(todo_path, f"# Setup TODO - {context.project_name}\n")
            separator = "\n---\n\n"
            append_text(todo_path, separator + self.content)
            return ActionResult(True)
        except (ValueError, OSError) as e:
            return ActionResult(False, f"{self.__class__.__name__} failed: {e}")