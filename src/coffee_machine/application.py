#!/usr/bin/env python
from collections.abc import Callable
from dataclasses import dataclass

from .exception.decorator.abort_decorator import AbortDecorator
from .order_data import DrinkType, ItemSpecs
from .orders import OrderDirector
from .prompt import get_prompt
from .resources import RESOURCES
from .style.decorator_type import DecoratorType


@dataclass()
class Status:
    is_on: bool
    profit: float


MENU: dict[str, ItemSpecs] = DrinkType.as_dict()

MENU_ITEMS = tuple(drink_name for drink_name in MENU)

STATUS = Status(is_on=True, profit=0.0)


@DecoratorType.PRINT_IN_RED()
def on_invalid_option() -> str:
    return "Please select a valid option."


@DecoratorType.COLORIZE_IN_GREEN()
def request_order():
    return f"What would you like? ({'/'.join(MENU_ITEMS)}): "


@DecoratorType.FIGLETIZE_TITLE()
def get_title():
    return "JavaGenie"


def process_drink_order(user_choice: str):
    order_director = OrderDirector(user_choice)
    order_director.process_order()
    STATUS.profit += order_director.profit


@DecoratorType.PRINT_IN_YELLOW()
def get_report():
    RESOURCES.get_all_info()
    return f"Money: ${STATUS.profit:.2f}"


@DecoratorType.PRINT_IN_YELLOW()
def turn_off():
    STATUS.is_on = False
    return "Thank you!"


@AbortDecorator()
def coffee_machine() -> None:
    """Main function to run the coffee machine."""
    while STATUS.is_on:
        user_choice = get_prompt(request_order(), str)
        options = {
            "quit": turn_off,
            "report": get_report,
        }
        if handler := options.get(user_choice):
            handler()
            continue

        if user_choice not in MENU:
            on_invalid_option()

        if user_choice in MENU:
            DrinkType.item_info(user_choice)
            process_drink_order(user_choice)


def run():
    functions: tuple[Callable, ...] = (get_title, coffee_machine)
    for function in functions:
        if callable(function):
            function()


if __name__ == "__main__":
    run()
