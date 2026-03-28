from .base import Plugin
from setup_context import SetupContext
from actions import Action

class ReactRouterPlugin(Plugin):
    key="react-router"
    display_name="React Router"
    description="Adds React Router with basic routing structure and example pages."

    def is_available(self, context: SetupContext) -> bool:
        return context.project_type == "Web App"

    def build_actions(self, context: SetupContext) -> list[Action]:
        pass