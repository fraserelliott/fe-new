from actions.base import Action, ActionPhase, ActionResult
from setup_context import SetupContext
from utils.path_utils import resolve_path

class AssertDirectoryAction(Action):
    """
    Checks whether a directory exists at the specified path.
    """
    
    def __init__(self, path: str) -> None:
        super().__init__(ActionPhase.SCAFFOLD)
        self.path = path
    
    def execute(self, context: SetupContext) -> ActionResult:
        try:
            full_path = resolve_path(self.path, context.parent_dir)
            if not full_path.exists():
                return ActionResult(False, f"{self.__class__.__name__} failed: directory does not exist at '{full_path}'")
            if not full_path.is_dir():
                return ActionResult(False, f"{self.__class__.__name__} failed: path is not a directory at '{full_path}'")
            return ActionResult(True)
        except (ValueError, OSError) as e:
            return ActionResult(False, f"{self.__class__.__name__} failed for '{self.path}': {e}")