# src/ota_installer/decorators/colorizer.py
from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps

from ..rich_colors import RichColors
from .protocol.decorator_protocols import StringReturningDecorator

type R = str


@dataclass
class Colorizer(StringReturningDecorator):
    """
    Colorizer decorator — applies ANSI style to the result of string-returning
    functions.
    """

    style: RichColors

    def __post_init__(self) -> None:
        """Initializes the color attribute based on the provided style."""
        self.color = self.style
        if self.color is None:
            raise ValueError(f"Invalid style: {self.style}")

    def __call__(self, func: Callable) -> Callable:
        """Wraps the function to apply color styling to its return value."""

        @wraps(func)
        def wrapper(*args, **kwargs) -> R:
            """
            Wrapper function that executes the original function and styles
            its output.
            """
            result = func(*args, **kwargs)
            return f"{self.color.beginning()}{result}{self.color.ending()}"

        return wrapper


def main() -> None:
    # Example usage
    colorizer = Colorizer(style=RichColors.BOLD_GREEN)

    @colorizer
    def greet(name: str) -> str:
        return f"Hello, {name}!"

    print(greet("Alice"))


if __name__ == "__main__":
    main()

# Signed off by Brian Sanford on 20260625
