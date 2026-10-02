# src/ota_installer/decorators/multiply_string.py
from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps

from .protocol.decorator_protocols import GenericDecorator

type R = str


@dataclass
class MultiplyString(GenericDecorator):
    """Decorator to multiply the string result of a function."""

    interval: int = 0

    def __call__(self, func: Callable) -> Callable:
        """Wraps the function to multiply its string result."""

        @wraps(func)
        def wrapper(*args, **kwargs) -> R:
            result = func(*args, **kwargs)
            return (
                str(result) * self.interval
                if self.interval > 0
                else str(result)
            )

        return wrapper


# Signed off by Brian Sanford on 20260625
