# src/ota_installer/style/rich_colors.py
from enum import StrEnum, auto


class RichColors(StrEnum):
    """Enumeration for rich color styles."""

    BOLD_GREEN = "green bold"
    BOLD_RED = "red bold"
    YELLOW = auto()
    WHITE = auto()

    def tag(self, closing: bool = False) -> str:
        """Constructs the tag for the rich style."""
        return f"[/{self.value}]" if closing else f"[{self.value}]"

    def beginning(self):
        """Constructs the beginning tag for the rich style."""
        return self.tag()

    def ending(self):
        """Constructs the ending tag for the rich style."""
        return self.tag(closing=True)


# src/ota_installer/style/rich_colors.py
