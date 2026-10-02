# src/ota_installer/protocols/decorators.py
from collections.abc import Callable
from typing import Protocol, TypeVar

R = TypeVar("R")

"""
Shared Protocols for decorator typing.
These are intended to be used with class-based decorators implementing
__call__.
"""


class GenericDecorator(Protocol[R]):
    """GenericDecorator: for decorators that preserve the return type."""

    def __call__(self, func: Callable[..., R]) -> Callable[..., R]: ...


class StringReturningDecorator(Protocol):
    """
    StringReturningDecorator: for decorators that transform or always return
    str.
    """

    def __call__(self, func: Callable[..., str]) -> Callable[..., str]: ...


# Signed off by Brian Sanford on 20260625
