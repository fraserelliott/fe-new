from setup_context import SetupContext
from utils.prompting import ask_text, select

project_options = {
    "Web App": {
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
    project_path = ask_text("Project directory:")
    project_types = list(project_options.keys())
    project_type = select("Project type:", project_types)
    languages = list(project_options[project_type].keys())
    language = select("Language:", languages)
    config = project_options[project_type][language]
    scaffold = select("Scaffold:", config["scaffolds"])
    package_manager = select("Package manager:", config["package_managers"])
    return SetupContext(project_name, project_path, project_type, language, scaffold, package_manager)