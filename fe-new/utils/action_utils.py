from actions import InstallAction, CreateFileAction, TodoAction
from utils.file_utils import read_text_file
from typing import Optional

def npm_install_action(*packages: str) -> InstallAction:
    return InstallAction(["npm", "install", *packages])

def copy_template_action(template_path: str, output_path: str, context: Optional[dict[str,str]] = None) -> CreateFileAction:
    content = read_text_file(template_path)
    if context:
        content = render_template(content, context)
    return CreateFileAction(output_path, content)

def todo_template_action(template_path: str, context: Optional[dict[str,str]] = None) -> TodoAction:
    content = read_text_file(template_path)
    if context:
        content = render_template(content, context)
    return TodoAction(content)

def render_template(content: str, context: dict[str, str]) -> str:
    for key, value in context.items():
        content = content.replace(f"{{{key}}}", value)
    return content