# src/ota_installer/decorators/double_padded_footer_wrapper.py
from collections.abc import Callable
from dataclasses import dataclass, field
from functools import wraps

from ...log_setup import LogType
from .container.decorator_container import Decorators
from .protocol.decorator_protocols import GenericDecorator


@dataclass
class DoublePaddedFooterWrapper(GenericDecorator):
    """
    Decorator that adds a double padded footer to the output of a function.
    """

    beginning: str = field(default="")
    message: str = field(default="Finished!")
    ending: str = field(default="")

    def __call__(self, func: Callable) -> Callable:
        """Wraps the function to add a double padded footer."""

        @wraps(func)
        def wrapper(*args, **kwargs) -> object:
            result = func(*args, **kwargs)
            self._print_footer(self.beginning)
            LogType.SUCCESS.write(self.message.strip())
            self._print_footer(self.message)
            self._print_footer(self.ending)
            return result

        return wrapper

    @Decorators.output_printer(use_color=False)
    @Decorators.colorizer(style="variable")
    @Decorators.indent_wrapper(interval=1)
    def _print_footer(self, message: str) -> str:
        """Outputs the footer messages."""
        return message


if __name__ == "__main__":
    pass

# Signed off by Brian Sanford on 20260625
