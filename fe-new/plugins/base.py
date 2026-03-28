from abc import ABC, abstractmethod
from actions import Action
from setup_context import SetupContext

class Plugin(ABC):
    """
    Base class for all project setup plugins.

    A plugin represents an optional, self-contained unit of functionality that can be
    included during project generation. Plugins are responsible for determining whether
    they are applicable to the current setup context and for contributing actions that
    extend the base project scaffold.

    Plugins are intentionally simple:
    - They do not depend on other plugins.
    - They do not maintain persistent configuration state.
    - Any required user input should be prompted within `build_actions()`.

    Attributes:
        key (str):
            Unique identifier for the plugin. Used internally for referencing the plugin.

        display_name (str):
            Human-readable name shown in CLI prompts.

        description (str):
            Short description of what the plugin provides, shown during selection.

    Methods:
        is_available(context: SetupContext) -> bool:
            Determines whether the plugin should be offered to the user based on the
            current setup context (e.g. language, project type, scaffold).

        build_actions(context: SetupContext) -> list[Action]:
            Builds and returns a list of actions required to apply the plugin.

            This method may prompt the user for any additional plugin-specific input
            needed to construct its actions. It should not perform side effects directly;
            all work must be expressed through returned Action instances.
    """
    key: str
    display_name: str
    description: str

    @abstractmethod
    def is_available(self, context: SetupContext) -> bool:
        pass

    @abstractmethod
    def build_actions(self, context: SetupContext) -> list[Action]:
        pass