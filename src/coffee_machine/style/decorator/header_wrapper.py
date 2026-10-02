# src/ota_installer/decorators/header_wrapper.py
from collections.abc import Callable
from dataclasses import dataclass, field
from functools import wraps

from .protocol.decorator_protocols import GenericDecorator


@dataclass
class HeaderWrapper(GenericDecorator):
    """Decorator that wraps a function with a header message output."""

    message: str = field(default="")

    from . import Colorizer  # Wrapper as DoubleWrapper
    from .indent_wrapper import IndentWrapper
    from .output_printer import OutputPrinter

    def __call__(self, func: Callable) -> Callable:
        """Wraps the function to display a header message before execution."""

        @wraps(func)
        def wrapper(*args, **kwargs) -> object:
            self._output_message()
            return func(*args, **kwargs)

        return wrapper

    @OutputPrinter(use_color=True)
    @Colorizer(style="variable")
    @IndentWrapper(interval=1)  # type: ignore[return-value]
    def _output_message(self) -> str:
        """Outputs the header message."""
        return self.message


# Signed off by Brian Sanford on 20260625
