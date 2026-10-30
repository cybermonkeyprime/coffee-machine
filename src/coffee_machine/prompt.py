from typing import overload

from rich.console import Console

from .style.decorator_type import DecoratorType


@overload
def get_prompt(*, message: str, target_type: type[int]) -> int: ...


@overload
def get_prompt(*, message: str, target_type: type[str]) -> str: ...


def get_prompt(
    *, message: str, target_type: type[int] | type[str]
) -> int | str:
    console = Console()

    while True:
        user_input: str = console.input(prompt=message).strip()

        if not user_input:
            return 0 if target_type is int else ""

        if target_type is int:
            return int(user_input)

            invalid_response(target_type=int)

        if target_type is str:
            if user_input.isalpha():
                return user_input

            invalid_response(target_type=str)


@overload
def invalid_response(*, target_type: type[int]) -> int: ...


@overload
def invalid_response(*, target_type: type[str]) -> str: ...


@DecoratorType.PRINT_IN_RED()
def invalid_response(target_type: type[int] | type[str]) -> int | str:
    value: str = "only numbers" if target_type is int else "only text"
    return f"Invalid option! Please enter {value}."
