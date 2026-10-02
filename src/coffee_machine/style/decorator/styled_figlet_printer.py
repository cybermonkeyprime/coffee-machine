# src/ota_installer/decorators/styled_figlet_printer.py
from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps

from coffee_machine.style.rich_colors import RichColors

from .figletizer import FontType
from .protocol.decorator_protocols import GenericDecorator


@dataclass
class StyledFigletPrinter(GenericDecorator):
    """Decorator for printing styled figlet text."""

    style: RichColors = RichColors.VARIABLE
    font: FontType = FontType.SLANT
    end: str = "\n"
    use_output: bool = False

    def __call__(self, func: Callable) -> Callable:
        """Wraps the function to apply figlet and color styles."""
        from . import Colorizer, Figletizer
        from .output_printer import OutputPrinter

        decorated_func = Figletizer(font=self.font)(func)  # type: ignore[reportArgumentType]
        decorated_func = Colorizer(style=self.style)(decorated_func)

        if self.use_output:
            decorated_func = OutputPrinter(suffix=self.end)(decorated_func)

        return wraps(func)(decorated_func)


@StyledFigletPrinter(
    style=RichColors.VARIABLE, font=FontType.SLANT, use_output=True
)
def welcome_message() -> str:
    """Returns a welcome message for the OTA Installer."""
    return "OTA Installer ready!"


if __name__ == "__main__":
    welcome_message()

# Signed off by Brian Sanford on 20260626
