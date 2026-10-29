#!/usr/bin/env python
from collections.abc import Callable
from dataclasses import dataclass

from .drinks import DRINK_CONFIG, DrinkType
from .exception.decorator.abort_decorator import AbortDecorator
from .orders import OrderDirector
from .prompt import get_prompt
from .resources import RESOURCES
from .style.decorator_type import DecoratorType
from .versioning.version_config import SoftwareVersion


@DecoratorType.FIGLETIZE_TITLE()
def get_title() -> str:
    return SoftwareVersion.TITLE.value


@DecoratorType.PRINT_IN_RED()
def on_invalid_option() -> str:
    return "Please select a valid option."


@DecoratorType.COLORIZE_IN_GREEN()
def request_order() -> str:
    return f"What would you like? ({'/'.join(DRINK_CONFIG.keys())}): "


@dataclass(slots=True)
class Status:
    is_on: bool
    profit: float


STATUS = Status(is_on=True, profit=0.0)


@DecoratorType.PRINT_IN_YELLOW()
def get_report() -> str:
    RESOURCES.get_all_info()
    return f"Money: ${STATUS.profit:.2f}"


@DecoratorType.PRINT_IN_YELLOW()
def turn_off() -> str:
    STATUS.is_on = False
    return "Thank you!"


def process_drink_order(user_choice: str) -> None:
    order_director = OrderDirector(user_choice)
    order_director.process_order()
    STATUS.profit += order_director.profit


@AbortDecorator()
def coffee_machine() -> None:
    """Main function to run the coffee machine."""
    options: dict[str, Callable] = {
        "quit": turn_off,
        "report": get_report,
    }
    while STATUS.is_on:
        user_choice = get_prompt(request_order(), str)
        if handler := options.get(user_choice):
            handler()
            continue

        if user_choice not in DRINK_CONFIG:
            on_invalid_option()

        if user_choice in DRINK_CONFIG:
            DrinkType[user_choice.upper()].item_price()
            process_drink_order(user_choice)


def run() -> None:
    functions: tuple[Callable, ...] = (
        SoftwareVersion.header,
        coffee_machine,
    )

    for function in functions:
        if callable(function):
            function()


if __name__ == "__main__":
    run()
