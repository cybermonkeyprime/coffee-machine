# src/ota_installer/decorators/confirmation_prompt.py
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import StrEnum
from functools import wraps

import pyinputplus as pyip
from rich.console import Console

from ..rich_colors import RichColors
from ..style_renderer import indentation

console = Console()


class PromptType(StrEnum):
    KEY_OPTION = "y/N"
    ERROR = "Invalid Option!"
    REQUEST = "Do you want to "
    EXECUTE = "execute the command"


@dataclass(frozen=True, slots=True)
class ConfirmationPrompt:
    """
    Decorator to prompt for user confirmation before executing a function.
    """

    begin: str = field(default="")
    comment: str = field(default="")
    indent: int = field(default=0)
    char: str = field(default="")
    debug: bool = field(default=False)
    style: str = field(default="")
    auto_confirm: bool = False

    def get_request(self, action: str) -> str:
        """Construct the prompt message."""
        return f"{PromptType.REQUEST.value}{action}"

    def get_key_option(self) -> str:
        """Return a string of valid key options."""
        style = RichColors["non_error".upper()]
        return f"{style.beginning()}{PromptType.KEY_OPTION}{style.ending()}"

    def get_message(self) -> str:
        """Construct the prompt message."""
        message = self.comment or PromptType.EXECUTE
        return (
            f"{indentation(self.indent)}{self.get_request(message)}? "
            f"[{self.get_key_option()}]: "
        )

    @staticmethod
    def get_confirmation() -> bool:
        """Get user confirmation input."""
        return pyip.inputYesNo(default="no", limit=3, blank=True) == "yes"

    def get_display(self) -> None:
        """Display the confirmation prompt message."""
        from . import Colorizer

        def func():
            return self.get_message()

        decorated_func = Colorizer(style="task")(func)
        console.print(decorated_func(), end="")

    @staticmethod
    def on_error() -> str:
        """Return the message for invalid options."""
        from . import Colorizer
        from .indent_wrapper import IndentWrapper

        def func():
            return PromptType.ERROR

        decorated_func = Colorizer(style="variable")(func)
        decorated_func = IndentWrapper(interval=1)(decorated_func)

        return decorated_func()

    def __call__(self, func: Callable) -> Callable:
        """Wrap the function with a confirmation prompt."""

        @wraps(func)
        def wrapper(*args, **kwargs) -> Callable | None:
            self.get_display()
            if not self.auto_confirm and not self.get_confirmation():
                return None
            return func(*args, **kwargs)

        return wrapper


@ConfirmationPrompt(
    begin="Start process", comment="Are you sure", indent=2, style="info"
)
def my_function():
    """Function implementation."""
    pass


# Signed off by Brian Sanford on 20260625
