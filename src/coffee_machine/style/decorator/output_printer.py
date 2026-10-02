# src/ota_installer/decorators/output_printer.py
from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps

from rich.console import Console

from .protocol.decorator_protocols import GenericDecorator

console = Console()


@dataclass
class OutputPrinter(GenericDecorator):
    """Decorator for printing function output with optional styling."""

    prefix: str = ""
    use_color: bool = False
    suffix: str = "\n"
    color: str = "non_error"

    def __call__(self, func: Callable) -> Callable:
        """Wraps the function to print its output with specified formatting."""

        @wraps(func)
        def wrapper(*args, **kwargs) -> object:
            from ..rich_colors import RichColors

            style = RichColors[self.color.upper()]
            result = func(*args, **kwargs)

            if result is not None:
                console.print(
                    f"{style.beginning()}{self.prefix}{result}{style.ending()}",
                    highlight=False,
                    end=self.suffix,
                )
            return result

        return wrapper


# Signed off by Brian Sanford on 20260625
