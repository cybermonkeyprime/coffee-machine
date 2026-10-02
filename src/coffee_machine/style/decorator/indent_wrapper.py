# /src/ota_installer/decorators/indent_wrapper.py
from collections.abc import Callable
from dataclasses import dataclass

from ..style_renderer import StyleRenderer
from .protocol.decorator_protocols import StringReturningDecorator

type R = str


@dataclass
class IndentWrapper(StringReturningDecorator):
    """Decorator that adds indentation to the output of a function."""

    interval: int = 0
    char = " "
    spacing = 4

    def __call__(self, func: Callable) -> Callable:
        """Wraps the function to add indentation to its output."""

        def wrapper(*args, **kwargs) -> R:
            result = func(*args, **kwargs)
            return f"{self.indent()}{result}"

        return wrapper

    def indent(self):
        """Generates the indentation string."""

        return StyleRenderer(self.char, self.spacing, self.interval)()


# Signed off by Brian Sanford on 20260625
