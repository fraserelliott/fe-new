from .base import Plugin
from setup_context import SetupContext
from actions import Action, EnsureDirectoryAction
from utils.action_utils import npm_install_action, copy_template_action, todo_template_action

class ReactRouterPlugin(Plugin):
    key="react-router"
    display_name="React Router"
    description="Adds React Router with basic routing structure and example pages."

    def is_available(self, context: SetupContext) -> bool:
        return context.project_type == "React Web App"

    def build_actions(self, context: SetupContext) -> list[Action]:
        actions = []
        if context.language == "JavaScript":
            extension = ".jsx"
        elif context.language == "TypeScript":
            extension = ".tsx"
        else:
            raise ValueError(f"Unsupported language for React Router plugin: {context.language}")
        todo_context = { "app_filename": f"App{extension}" }
        actions.append(npm_install_action("react-router-dom"))
        actions.append(EnsureDirectoryAction("src/pages"))
        actions.append(copy_template_action("fe-new/templates/react-router/AppRouter.jsx.template", f"src/AppRouter{extension}"))
        actions.append(copy_template_action("fe-new/templates/react-router/HomePage.jsx.template", f"src/pages/HomePage{extension}"))
        actions.append(todo_template_action("fe-new/templates/react-router/todo.md", todo_context))
        return actions