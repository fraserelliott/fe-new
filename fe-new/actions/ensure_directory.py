from actions.base import Action, ActionPhase, ActionResult
from setup_context import SetupContext
from utils.path_utils import resolve_path

class EnsureDirectoryAction(Action):
    """
    Ensures a directory exists at the specified path.

    Rules:
    - If the directory does not exist, it is created.
    - If the directory already exists, the action succeeds.
    - The path must resolve within the project root; otherwise execution fails.
    - If the directory cannot be created due to filesystem or permission issues, the action fails.
    - This action does not modify or remove existing directories.

    Returns:
        True if the directory exists or was successfully created.
        False if the directory could not be created or the path is invalid.
    """
    phase = ActionPhase.CREATE_DIRECTORY
    
    def __init__(self, path: str) -> None:
        self.path = path
    
    def execute(self, context: SetupContext) -> ActionResult:
        try:
            resolved = resolve_path(self.path, context.project_dir)
            resolved.mkdir(parents=True, exist_ok=True)
            return ActionResult(True)
        except (ValueError, OSError) as e:
            return ActionResult(False, f"{self.__class__.__name__} failed for '{self.path}': {e}")