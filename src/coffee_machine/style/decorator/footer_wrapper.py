# src/ota_installer/decorators/footer_wrapper.py
from collections.abc import Callable
from dataclasses import dataclass, field
from functools import wraps


@dataclass
class FooterWrapper:
    """Decorator that wraps a function with a footer message output."""

    message: str = field(default="")

    from . import Colorizer  # Wrapper as DoubleWrapper
    from .indent_wrapper import IndentWrapper
    from .output_printer import OutputPrinter

    def __call__(self, function: Callable) -> Callable:
        """Wraps the given function to include footer message output."""

        @wraps(function)
        def wrapper(*args, **kwargs) -> object:
            result = function(*args, **kwargs)
            self._output_message()
            return result

        return wrapper

    @OutputPrinter(use_color=True)
    @Colorizer(style="variable")
    @IndentWrapper(interval=1)  # type: ignore[return-value]
    def _output_message(self) -> str:
        """Outputs the footer message."""
        return self.message


# Signed off by Brian Sanford on 20260628
