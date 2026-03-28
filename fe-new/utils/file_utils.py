from pathlib import Path
from typing import Callable
import os

def read_text_file(path: Path, encoding: str="utf-8") -> str:
    with open(path, "r", encoding=encoding) as f:
        return f.read()

def safe_write_text_file(path: Path, content: str, encoding: str="utf-8") -> None:
    tmp_path = path.with_name(path.name + ".tmp")
    path.parent.mkdir(parents=True, exist_ok=True)
    with tmp_path.open("w", encoding=encoding) as f:
        f.write(content)
    os.replace(tmp_path, path)

def transform_file(path: Path, transform: Callable[[str], str], encoding: str = "utf-8") -> None:
    original = read_text_file(path, encoding)
    updated = transform(original)
    safe_write_text_file(path, updated, encoding=encoding)

def append_text(path: Path, content: str):
    def transform(existing):
        if not existing.endswith("\n"):
            existing += "\n"
        return existing + content
    transform_file(path, transform)

def prepend_text(path: Path, content: str):
    def transform(existing):
        if not content.endswith("\n"):
            content_with_newline = content + "\n"
        else:
            content_with_newline = content
        return content_with_newline + existing
    transform_file(path, transform)