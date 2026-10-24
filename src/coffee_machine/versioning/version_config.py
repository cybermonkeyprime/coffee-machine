# src/ota_installer/handler/version_handler.py
from enum import Enum

from ..style.decorator_type import DecoratorType


class SoftwareVersion(Enum):
    """Enumeration for software version constants."""

    TITLE = "JavaGenie"

    @classmethod
    def to_dict(cls) -> dict:
        return {
            name.lower(): member.value
            for name, member in cls.__members__.items()
        }

    @classmethod
    @DecoratorType.FIGLETIZE_TITLE()
    def header(cls):
        return cls.TITLE.value


# Signed off by Brian Sanford on 20260917
