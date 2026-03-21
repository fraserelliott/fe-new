from pathlib import Path

def resolve_path(path: str, root_dir: str) -> Path:
    root = Path(root_dir).resolve()
    full = (root / path).resolve()

    if not str(full).startswith(str(root)):
        raise ValueError("Path escapes root directory")

    return full