from dataclasses import dataclass

@dataclass
class SetupContext:
    project_name: str
    project_path: str
    project_type: str
    language: str
    scaffold: str
    package_manager: str