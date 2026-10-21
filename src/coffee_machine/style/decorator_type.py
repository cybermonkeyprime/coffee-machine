from enum import Enum
from functools import partial

from . import decorator
from .decorator.figletizer import FontType
from .rich_colors import RichColors

print_in_color = partial(
    decorator.StylizedIndentPrinter, indent=1, use_output=True
)

input_in_color = partial(
    decorator.StylizedIndentPrinter, indent=2, use_output=False
)
padded_print = partial(print_in_color, begin="", end="\n\n")


class DecoratorType(Enum):
    PRINT_TITLE = decorator.StyledFigletPrinter(
        font=FontType.SLANT, use_output=True, style=RichColors.YELLOW
    )
    PRINT_IN_YELLOW = print_in_color(style=RichColors.YELLOW, end="\n")
    PRINT_IN_GREEN = print_in_color(style=RichColors.BOLD_GREEN, end="\n\n")
    PRINT_IN_RED = print_in_color(style=RichColors.BOLD_RED, end="\n\n")
    INPUT_IN_YELLOW = input_in_color(style=RichColors.YELLOW)
    INPUT_IN_WHITE = input_in_color(style=RichColors.WHITE)
    PRINT_PADDED_YELLOW = padded_print(style=RichColors.YELLOW)
    PRINT_PADDED_RED = padded_print(style=RichColors.BOLD_RED)
