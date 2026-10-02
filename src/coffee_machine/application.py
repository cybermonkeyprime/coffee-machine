#!/usr/bin/env python
from dataclasses import dataclass

from rich.console import Console

from .exception.decorator.abort_decorator import AbortDecorator
from .order_data import MENU
from .orders import OrderDirector
from .resources import RESOURCES
from .style import decorator
from .style.decorator.figletizer import FontType
from .style.rich_colors import RichColors

task_decorator = decorator.StylizedIndentPrinter(
    style=RichColors.WARNING, indent=1, end="\n", use_output=True
)
title_decorater = decorator.StyledFigletPrinter(
    font=FontType.SLANT, use_output=True, style=RichColors.VARIABLE
)


MENU_ITEMS = tuple(drink_name for drink_name in MENU)


@decorator.Colorizer(style=RichColors.TASK)
def user_input():
    return f"What would you like? ({'/'.join(MENU_ITEMS)}): "


@title_decorater
def get_title():
    return "JavaGenie"


@dataclass()
class Status:
    is_on: bool
    profit: float


STATUS = Status(is_on=True, profit=0.0)


def process_drink_order(user_choice: str):
    order_director = OrderDirector(user_choice)
    order_director.process_order()
    STATUS.profit += order_director.profit


@AbortDecorator()
def coffee_machine() -> None:
    """Main function to run the coffee machine."""
    console = Console()
    while STATUS.is_on:
        user_choice = console.input(user_input())
        options = {
            "quit": turn_off,
            "report": get_report,
        }
        if handler := options.get(user_choice):
            handler()
            continue
        if user_choice in MENU:
            process_drink_order(user_choice)


@task_decorator
def get_report():
    RESOURCES.get_all_info()
    return f"Money: ${STATUS.profit:.2f}"


@task_decorator
def turn_off():
    STATUS.is_on = False
    return "Thank you!"


def run():
    get_title()
    coffee_machine()


if __name__ == "__main__":
    run()
