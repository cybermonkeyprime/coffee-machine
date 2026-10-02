# src/ota_installer/style/style_renderer.py
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class StyleRenderer:
    """Container for style attributes."""

    character: str
    spacing: int
    interval: int

    def __call__(self) -> str:
        """Creates an indentation string."""
        return self.character * self.spacing * self.interval


SEPARATOR = StyleRenderer(character="-", spacing=4, interval=10)


def indentation(interval: int = 1, char: str = " ", spaces: int = 4) -> str:
    """Creates an indentation string."""
    return StyleRenderer(char[0], spaces, interval)()


def separator(cls: StyleRenderer = SEPARATOR) -> str:
    """Generates a formatted separator string."""
    return cls()


# Signed off by Brian Sanford on 20260831
