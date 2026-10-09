# src/ota_installer/decorators/styled_indent_printer.py
from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps

from ..rich_colors import RichColors
from .protocol.decorator_protocols import GenericDecorator


@dataclass
class StylizedIndentPrinter(GenericDecorator):
    """
    Decorator that applies stylized indentation and colorization to a
    function's output.
    """

    style: RichColors = RichColors.YELLOW
    indent: int = 0
    begin: str = ""
    end: str = ""
    use_output: bool = False

    def __call__(self, func: Callable) -> Callable:
        """
        Wraps the given function with stylized indentation and colorization.
        """
        from . import Colorizer, IndentWrapper
        from .output_printer import OutputPrinter

        decorated_func = IndentWrapper(interval=self.indent)(func)  # pyright: ignore[reportArgumentType]
        decorated_func = Colorizer(style=self.style)(decorated_func)

        if self.use_output:
            decorated_func = OutputPrinter(suffix=self.end)(decorated_func)

        return wraps(func)(decorated_func)


# Signed off by Brian Sanford on 20260625
