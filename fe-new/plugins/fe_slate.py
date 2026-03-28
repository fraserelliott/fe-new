from .base import Plugin
from setup_context import SetupContext
from actions import Action

class FeSlatePlugin(Plugin):
    key="fe-slate"
    display_name="fe-slate"
    description="Sets up Sequelize ORM with initial configuration and environment variables."

    def is_available(self, context: SetupContext) -> bool:
        return context.project_type == "Web App"

    def build_actions(self, context: SetupContext) -> list[Action]:
        pass