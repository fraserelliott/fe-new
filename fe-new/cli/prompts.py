from setup_context import SetupContext
from utils.prompting import ask_text, select
from runner import Runner
from actions import ScaffoldAction, EnsureDirectoryAction, InstallAction, AssertDirectoryAction, ActionPhase
from pathlib import Path
import re

project_options = {
    "React Web App": {
        "JavaScript": {
            "scaffolds": ["Vite"],
            "package_managers": ["npm"]
        },
        "TypeScript": {
            "scaffolds": ["Vite"],
            "package_managers": ["npm"]
        }
    },
    "Server": {
        "JavaScript": {
            "scaffolds": ["npm"],
            "package_managers": ["npm"]
        },
        "TypeScript": {
            "scaffolds": ["npm"],
            "package_managers": ["npm"]
        }
    },
    "Command Line": {
        "Python": {
            "scaffolds": [],
            "package_managers": ["pip"]
        }
    }
}

def run_prompts():
    project_name = ask_text("Project name:")
    parent_dir = Path(ask_text("Parent directory:"))
    project_dir = parent_dir / project_name
    project_types = list(project_options.keys())
    project_type = select("Project type:", project_types)
    languages = list(project_options[project_type].keys())
    language = select("Language:", languages)
    config = project_options[project_type][language]
    scaffold = select("Scaffold:", config["scaffolds"])
    package_manager = select("Package manager:", config["package_managers"])
    return SetupContext(project_name, parent_dir, project_dir, project_type, language, scaffold, package_manager)

def build_runner(context: SetupContext):
    runner = Runner(context)
    if context.scaffold == "Vite":
        template = "react" if context.language == "JavaScript" else "react-ts"
        command = ["npm", "create", "vite@latest", context.project_name, "--", "--template", template, "--no-interactive"]
        runner.add_action(ScaffoldAction(command, None, True))
        runner.add_action(InstallAction(["npm", "install"]))
    elif context.scaffold == "npm":
        runner.add_action(EnsureDirectoryAction(".", ActionPhase.SCAFFOLD))
        command = ["npm", "init", "-y"]
        runner.add_action(ScaffoldAction(command))
        if context.project_type == "Server":
            pass
    elif context.scaffold is None:
        runner.add_action(EnsureDirectoryAction(".", ActionPhase.SCAFFOLD))
        if context.language == "Python":
            runner.add_action(ScaffoldAction(["python", "-m", "venv", ".venv"]))
        else:
            raise ValueError(f"No default scaffold defined for {context.language}")
    else:
        raise ValueError(f"Unsupported scaffold: {context.scaffold}")
    runner.add_action(AssertDirectoryAction(context.project_dir))
    return runner