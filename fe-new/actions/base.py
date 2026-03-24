from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
from enum import IntEnum
from setup_context import SetupContext

@dataclass
class ActionResult:
    success: bool
    message: Optional[str] = None

class ActionPhase(IntEnum):
    SCAFFOLD = 10
    CREATE_DIRECTORY = 20
    INSTALL = 30
    CREATE_FILE = 40
    UPDATE_FILE = 50

class Action(ABC):
    """
    Base class for all actions.

    Action contract:
    - Each action represents a single, clear intent.
    - execute() returns True only if that intent was satisfied.
    - Idempotent success is allowed, but actions must not silently drop intent.
    - Actions catch expected operational errors and return False.
    - Actions must not perform hidden destructive behavior.
    - The runner is responsible for handling failures (e.g. stop or continue).
    """
    phase: int

    @abstractmethod
    def execute(self, context: SetupContext) -> ActionResult:
        pass