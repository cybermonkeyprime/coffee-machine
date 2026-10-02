# src/ota_installer/decorators/continue_on_keypress.py
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import StrEnum
from functools import wraps


class Message(StrEnum):
    PROMPT = "Press the Enter key to continue... "


@dataclass
class ContinueOnKeyPress:
    """Decorator that pauses execution until the user presses the Enter key."""

    indent: int = field(default=1)
    char: str = field(default=" ")

    from ...exception.decorator.exception_handler import ExceptionHandler
    from .colorizer import Colorizer
    from .output_printer import OutputPrinter

    @ExceptionHandler()
    def __call__(self, function: Callable) -> Callable:
        """Wraps the function to display a message and wait for user input."""

        @wraps(function)
        def wrapper(*args, **kwargs) -> object:
            result = function(*args, **kwargs)
            self.display_message()
            input()
            return result

        return wrapper

    def display_message(self) -> str:
        """Displays a message prompting the user to continue."""
        from .colorizer import Colorizer
        from .output_printer import OutputPrinter

        def func():
            return Message.PROMPT

        decorated_func = OutputPrinter(prefix="\n", suffix="")(func)
        decorated_func = Colorizer(style="title")(decorated_func)
        return decorated_func()


if __name__ == "__main__":
    pass

# Signed off by Brian Sanford on 20260626
