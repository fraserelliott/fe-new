from setup_context import SetupContext
from utils.prompting import ask_text, select
from runner import Runner
from actions import ScaffoldAction, EnsureDirectoryAction, InstallAction, AssertDirectoryAction, ActionPhase, CreateFileAction
from pathlib import Path
from utils.action_utils import npm_install_action, copy_template_action
import re
from dataclasses import dataclass
from typing import Callable

@dataclass
class ProjectConfig:
    scaffolds: list[str]
    package_managers: list[str]
    build_function: Callable

def run_prompts():
    project_name = ask_text("Project name:")
    parent_dir = Path(ask_text("Parent directory:"))
    project_dir = parent_dir / project_name
    project_types = list(project_options.keys())
    project_type = select("Project type:", project_types)
    languages = list(project_options[project_type].keys())
    language = select("Language:", languages)
    config = project_options[project_type][language]
    scaffold = select("Scaffold:", config.scaffolds)
    package_manager = select("Package manager:", config.package_managers)
    return SetupContext(project_name, parent_dir, project_dir, project_type, language, scaffold, package_manager)

def build_runner(context: SetupContext):
    config = project_options[context.project_type][context.language]
    runner = config.build_function(context)
    runner.add_action(AssertDirectoryAction(context.project_dir))
    return runner    

def build_react_app(context: SetupContext) -> Runner:
    runner = Runner(context)
    template = "react" if context.language == "JavaScript" else "react-ts"
    command = ["npm", "create", "vite@latest", context.project_name, "--", "--template", template, "--no-interactive"]
    runner.add_action(ScaffoldAction(command, None, True))
    runner.add_action(InstallAction(["npm", "install"]))
    return runner

def build_express_server(context: SetupContext) -> Runner:
    runner = Runner(context)
    package_context = { "project_name": context.project_name }
    runner.add_action(copy_template_action("fe-new/templates/server-js/package.json.template", "package.json", package_context, ActionPhase.SCAFFOLD))
    runner.add_action(EnsureDirectoryAction(".", ActionPhase.SCAFFOLD))
    runner.add_action(EnsureDirectoryAction("config"))
    runner.add_action(EnsureDirectoryAction("middleware"))
    runner.add_action(EnsureDirectoryAction("routes"))
    runner.add_action(EnsureDirectoryAction("scripts"))
    runner.add_action(npm_install_action("cors", "express", "dotenv"))
    runner.add_action(npm_install_action("cross-env", "nodemon", install_dev_dependencies=True))
    runner.add_action(copy_template_action("fe-new/templates/server-js/server.js.template", "server.js"))
    runner.add_action(copy_template_action("fe-new/templates/server-js/.env.template", ".env"))
    runner.add_action(copy_template_action("fe-new/templates/server-js/.env.template", ".env.example"))
    runner.add_action(copy_template_action("fe-new/templates/server-js/.gitignore.template", ".gitignore"))
    runner.add_action(copy_template_action("fe-new/templates/server-js/index.route.js.template", "routes/index.route.js"))
    return runner

def build_python_cli(context: SetupContext) -> Runner:
    runner = Runner(context)
    runner.add_action(EnsureDirectoryAction(".", ActionPhase.SCAFFOLD))
    runner.add_action(ScaffoldAction(["python", "-m", "venv", ".venv"]))
    return runner

project_options = {
    "React Web App": {
        "JavaScript": ProjectConfig(
            scaffolds=["Vite"],
            package_managers=["npm"],
            build_function=build_react_app
        ),
        "TypeScript": ProjectConfig(
            scaffolds=["Vite"],
            package_managers=["npm"],
            build_function=build_react_app
        )
    },
    "Express Server": {
        "JavaScript": ProjectConfig(
            scaffolds=[],
            package_managers=["npm"],
            build_function=build_express_server
        )
    },
    "Command Line": {
        "Python":  ProjectConfig(
            scaffolds=[],
            package_managers=["pip"],
            build_function=build_python_cli
        )
    }
}