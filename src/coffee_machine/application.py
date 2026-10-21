#!/usr/bin/env python
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


@AbortDecorator()
def coffee_machine() -> None:
    """Main function to run the coffee machine."""
    while STATUS.is_on:
        user_choice = get_prompt(user_input(), str)
        if MENU.get(user_choice) is None:
            on_invalid_option()
        else:
            drink_info(user_choice)
            options = {
                "quit": turn_off,
                "report": get_report,
            }
            if handler := options.get(user_choice):
                handler()
                continue
            if user_choice in MENU:
                process_drink_order(user_choice)


def drink_info(user_choice: str) -> None:
    DrinkType[user_choice.upper()].item_info()


@DecoratorType.PRINT_IN_RED()
def on_invalid_option() -> str:
    return "Please select a valid option."


@DecoratorType.COLORIZE_IN_GREEN()
def user_input():
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


def run():
    get_title()
    coffee_machine()


if __name__ == "__main__":
    run()
