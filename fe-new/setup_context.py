from dataclasses import dataclass
from pathlib import Path

@dataclass
class SetupContext:
    project_name: str
    parent_dir: Path
    project_dir: Path
    project_type: str
    language: str
    scaffold: str
    package_manager: str