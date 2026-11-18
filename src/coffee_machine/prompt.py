from typing import overload

from rich.console import Console

from .style.decorator_type import DecoratorType

TARGET_TYPE: type[TARGET_TYPE] = type[int | str]


@overload
def get_prompt(*, message: str, target_type: type[int]) -> int: ...


@overload
def get_prompt(*, message: str, target_type: type[str]) -> str: ...


def get_prompt(*, message: str, target_type: TARGET_TYPE) -> int | str:
    console = Console()

    while True:
        user_input: str = console.input(prompt=message).strip()

        if not user_input:
            return 0 if target_type is int else ""

        if target_type is int:
            try:
                return int(user_input)
            except ValueError:
                on_invalid_response(target_type=int)
                continue

        if target_type is str:
            if user_input.isalpha():
                return user_input

            on_invalid_response(target_type=str)


@overload
def on_invalid_response(*, target_type: type[int]) -> str: ...


@overload
def on_invalid_response(*, target_type: type[str]) -> str: ...


@DecoratorType.PRINT_IN_RED()
def on_invalid_response(target_type: TARGET_TYPE) -> str:
    output_type: str = "numbers" if target_type is int else "text"
    return f"Invalid option! Please enter only {output_type}."
