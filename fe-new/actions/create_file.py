from actions.base import Action, ActionPhase, ActionResult
from setup_context import SetupContext
from typing import Optional
from utils.path_utils import resolve_path
from utils.file_utils import safe_write_text_file

class CreateFileAction(Action):
    """
    Ensures a file exists at the specified path.

    If content is provided, the action also defines an intent to create the file
    with that initial content.

    Rules:
    - If the file does not exist:
        - The file is created.
        - If content is provided, it is written to the file.
    - If the file already exists and no content is provided, the action succeeds.
    - If the file already exists and content is provided, the action fails.
    - The path must resolve within the project root; otherwise execution fails.
    - If the file cannot be created due to filesystem or permission issues, the action fails.
    - This action never modifies existing files.

    Returns:
        True if the file exists or was successfully created.
        False if the action could not satisfy its intent (e.g. conflicting content or invalid path).
    """

    def __init__(self, path: str, content: Optional[str] = None, phase: Optional[ActionPhase] = ActionPhase.CREATE_FILE) -> None:
        super().__init__(phase)
        self.path = path
        self.content = content
    
    def execute(self, context: SetupContext) -> ActionResult:
        try:
            print(f"Creating file {self.path}")
            resolved = resolve_path(self.path, context.project_dir)
            if resolved.is_file():
                if self.content is None:
                    return ActionResult(True)
                return ActionResult(False, f"CreateFileAction failed for '{self.path}': cannot overwrite content of existing file.")
            if self.content is None:
                resolved.parent.mkdir(parents=True, exist_ok=True)
                resolved.touch()
                return ActionResult(True)
            safe_write_text_file(resolved, self.content)
            return ActionResult(True)
        except (ValueError, OSError) as e:
            return ActionResult(False, f"{self.__class__.__name__} failed for '{self.command}': {e}")