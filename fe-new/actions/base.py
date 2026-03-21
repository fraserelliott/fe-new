from abc import ABC, abstractmethod
from enum import IntEnum
from setup_context import SetupContext

class ActionPhase(IntEnum):
    SCAFFOLD = 10
    CREATE_DIRECTORY = 20
    INSTALL = 30
    CREATE_FILE = 40
    UPDATE_FILE = 50

class Action(ABC):
    phase: int

    @abstractmethod
    def execute(self, context: SetupContext):
        pass