from .base import Plugin
from setup_context import SetupContext
from actions import Action

class SequelizePlugin(Plugin):
    key="sequelize"
    display_name="Sequelize"
    description="Configures Sequelize with starter setup, environment variables, and project structure."
    
    def is_available(self, context: SetupContext) -> bool:
        return context.project_type == "Server"

    def build_actions(self, context: SetupContext) -> list[Action]:
        pass