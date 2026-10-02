# src/ota_installer/decorators/encapsulation.py
from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps

from .protocol.decorator_protocols import GenericDecorator


@dataclass
class Encapsulate(GenericDecorator):
    """Decorator class to encapsulate function calls with separators."""

    def __call__(self, func: Callable) -> Callable:
        """
        Wraps the function with separator calls before and after execution.
        """

        @wraps(func)
        def wrapper(*args, **kwargs) -> object:
            self._print_separator()
            result = func(*args, **kwargs)
            self._print_separator()
            return result

        return wrapper

    def _print_separator(self) -> str:
        """Prints a separator line."""
        from ..style_renderer import separator
        from .output_printer import OutputPrinter

        decorated_func = OutputPrinter(prefix="\n", suffix="\n\n")(separator)
        return decorated_func()


# Signed off by Brian Sanford on 20260625
