from pathlib import Path

def resolve_path(path: str | Path, root_dir: Path) -> Path:
    root = root_dir.resolve()
    full = (root / path).resolve()

    try:
        full.relative_to(root)
    except ValueError:
        raise ValueError("Path escapes root directory")

    return full