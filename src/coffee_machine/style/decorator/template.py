# src/ota_installer/decorators/template.py
from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps

from .protocol.decorator_protocols import GenericDecorator

type R = object


@dataclass
class Example(GenericDecorator):
    """A decorator class that logs the start and end of function execution."""

    func: Callable
    start_message: str = "Beginning"
    end_message: str = "Ending"

    def __call__(self, *args, **kwargs) -> Callable:
        """Wraps the function to log messages before and after execution."""
        name = getattr(self.func, __name__, "name")
        print(f"{self.start_message} {name}")
        result = self.func(*args, **kwargs)
        print(f"{self.end_message} {name}")
        return result


@dataclass
class ExampleWithArgs(GenericDecorator):
    """A decorator class that logs the start and end of function execution."""

    begin: str = "Beginning"
    end: str = "Ending"

    def __call__(self, func: Callable) -> Callable:
        """Wraps the function to log messages before and after execution."""

        @wraps(func)
        def wrapper(*args, **kwargs) -> Callable:
            name = getattr(func, __name__, "name")
            print(f"{self.begin} {name}")
            result = func(*args, **kwargs)
            print(f"{self.end} {name}")
            return result

        return wrapper


# Signed off by Brian Sanford on 20260625
