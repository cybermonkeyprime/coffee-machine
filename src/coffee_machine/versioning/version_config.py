# src/ota_installer/handler/version_handler.py
from dataclasses import dataclass
from enum import Enum


class SoftwareVersion(Enum):
    """Enumeration for software version constants."""

    TITLE = "OTA-Installer"
    MAJOR_NUMBER = 2026
    MINOR_NUMBER = 9
    PATCH_NUMBER = 1

    @classmethod
    def to_dict(cls) -> dict:
        return {
            name.lower(): member.value
            for name, member in cls.__members__.items()
        }

    @classmethod
    def render(cls):
        return SoftwareRenderer(**cls.to_dict())

    @classmethod
    def display(cls) -> str:
        return cls.render().fetch_normal_display()

    @classmethod
    def formatted(cls) -> str:
        return cls.render().fetch_formatted_display()

    @classmethod
    def version(cls) -> str:
        return cls.render().fetch_version_stats()


@dataclass(frozen=True)
class SoftwareRenderer:
    """Represents a software container with versioning information."""

    title: str
    major_number: int
    minor_number: int
    patch_number: int

    def fetch_version_stats(self) -> str:
        return f"{self.major_number}.{self.minor_number}.{self.patch_number}"

    def fetch_normal_display(self) -> str:
        """Returns the display string for the global software version."""
        return f"Build: {self.fetch_version_stats()}"

    def fetch_formatted_display(self) -> str:
        """
        Returns a formatted string with the title or display of the software
        version."""
        return f"{self.title} - {self.fetch_normal_display()}"


# Signed off by Brian Sanford on 20260917
