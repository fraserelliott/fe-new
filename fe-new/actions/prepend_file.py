from actions.base import Action, ActionPhase, ActionResult
from setup_context import SetupContext
from typing import Optional
from utils.path_utils import resolve_path
from utils.file_utils import prepend_text

class PrependFileAction(Action):
    """
    Prepends content to an existing file.

    Rules:
    - The file must already exist; otherwise execution fails.
    - The provided content is inserted at the beginning of the file.
    - The path must resolve within the project root; otherwise execution fails.
    - If the file cannot be read or written due to filesystem or permission issues,
    the action fails.
    - This action does not create files.

    Returns:
        True if content was successfully prepended.
        False if the file does not exist, the path is invalid, or the operation fails.
    """
    phase = ActionPhase.UPDATE_FILE

    def __init__(self, path: str, content: Optional[str] = None) -> None:
        self.path = path
        self.content = content
    
    def execute(self, context: SetupContext) -> ActionResult:
        try:
            print(f"Prepending file {self.path}")
            resolved = resolve_path(self.path, context.project_dir)
            if not resolved.is_file():
                return ActionResult(False, f"{self.__class__.__name__} failed for '{self.path}': file does not exist.")
            prepend_text(resolved, self.content)
            return ActionResult(True)
        except (ValueError, OSError) as e:
            return ActionResult(False, f"{self.__class__.__name__} failed for '{self.command}': {e}")