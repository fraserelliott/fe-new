from .base import Plugin
from setup_context import SetupContext
from actions import Action, PrependFileAction
from utils.action_utils import npm_install_action

class FeSlatePlugin(Plugin):
    key="fe-slate"
    display_name="fe-slate"
    description="Sets up Sequelize ORM with initial configuration and environment variables."

    def is_available(self, context: SetupContext) -> bool:
        return context.project_type == "React Web App"

    def build_actions(self, context: SetupContext) -> list[Action]:
        actions = []
        actions.append(npm_install_action("@fraserelliott/fe-slate"))
        if context.language == "JavaScript":
            filename = "src/main.jsx"
        else:
            filename = "src/main.tsx"
        actions.append(PrependFileAction(filename, "import '@fraserelliott/fe-slate';"))
        return actions