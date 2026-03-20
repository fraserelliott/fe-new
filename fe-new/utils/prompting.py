from InquirerPy import inquirer
from typing import Optional, TypeVar

T = TypeVar("T")

def ask_text(message:str) -> str:
    return inquirer.text(message=message).execute()

def ask_confirm(message:str, default: bool = True) -> bool:
    return inquirer.confirm(message=message, default=default).execute()

def ask_select(message: str, choices: list[T]) -> T:
    return inquirer.select(message=message, choices=choices).execute()

def select(message: str, choices: list[T]) -> Optional[T]:
    if len(choices) == 0:
        return None
    elif len(choices) == 1:
        print(f"{message} {choices[0]}")
        return choices[0]
    else:
        return ask_select(message, choices)

def ask_multi_select(message: str, choices: list[T]) -> list[T]:
    return inquirer.checkbox(message=message, choices=choices).execute()