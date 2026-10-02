# src/ota_installer/decorators/figletizer.py
from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum, auto
from functools import wraps

from pyfiglet import figlet_format


class FontType(StrEnum):
    SLANT = auto()


@dataclass(frozen=True, slots=True)
class Figletizer:
    """
    Decorator that formats the output of a function using a specified figlet
    font.
    """

    font: FontType = FontType.SLANT

    def __call__(self, func: Callable) -> Callable:
        """Wraps the given function to format its output with figlet."""

        @wraps(func)
        def wrapper(*args, **kwargs) -> str:
            """Calls the original function and formats its output."""
            result = func(*args, **kwargs)
            return figlet_format(str(result), font=FontType.SLANT)

        return wrapper


# Signed off by Brian Sanford on 20260627
