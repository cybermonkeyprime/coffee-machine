# src/ota_installer/decorators/timeit.py
import time
from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps

from .protocol.decorator_protocols import GenericDecorator


@dataclass
class TimeIt(GenericDecorator):
    """Decorator to measure the execution time of a function."""

    start_time: float = 0
    end_time: float = 0

    def __call__(self, func: Callable) -> Callable:
        """Wrap the function to measure its execution time."""

        @wraps(func)
        def wrapper(*args, **kwargs) -> object:
            self.start_time = time.perf_counter()
            result = func(*args, **kwargs)
            self.end_time = time.perf_counter()
            self._log_execution_time(func, args, kwargs)
            return result

        return wrapper

    def _log_execution_time(
        self, func: Callable, args: tuple, kwargs: dict
    ) -> None:
        """Log the execution time of the function."""
        total_time = self.end_time - self.start_time
        name = getattr(func, __name__, "func")
        function_signature = f"{name}{args} {kwargs}"
        print(f"Function {function_signature} took {total_time:.4f} seconds")


# Signed off by Brian Sanford on 20260626
