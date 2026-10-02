# src/ota_installer/exception/decorator/exception_decorator.py
from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps

from ...style import decorator as style
from ...style.rich_colors import RichColors
from ...style.style_renderer import indentation
from .protocol.decorator_protocols import GenericDecorator


@dataclass(frozen=True, slots=True)
class AbortDecorator(GenericDecorator):
    """Handle a specific exception and display a styled message."""

    def __call__(self, function: Callable) -> Callable:
        @wraps(function)
        def wrapper(*args, **kwargs) -> object | None:
            try:
                return function(*args, **kwargs)
            except (EOFError, KeyboardInterrupt) as exception:
                self.display_message(exception)
                return None

        return wrapper

    def display_message(self, exception: BaseException) -> None:
        line_break = "\n\n"
        exception = type(exception).__name__

        def message() -> str:
            return (
                f"{line_break}"
                f"{indentation()}{exception} detected, aborting safely"
                f"{line_break}"
            )

        decorated = style.StylizedIndentPrinter(
            style=RichColors.WARNING,
            indent=1,
            use_output=True,
        )(message)

        decorated()


# Signed off by Brian Sanford on 20260912
