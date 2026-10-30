#!/usr/bin/env python
from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum

from .drinks import DRINK_CONFIG, DrinkType
from .exception.decorator.abort_decorator import AbortDecorator
from .orders import OrderDirector
from .prompt import get_prompt
from .resources import RESOURCES
from .style.decorator_type import DecoratorType
from .versioning.version_config import SoftwareVersion


@dataclass(slots=True)
class Status:
    is_on: bool
    profit: float


class StrType(StrEnum):
    INVALID_OPTION = "Please select a valid option."
    REQUEST_ORDER = f"What would you like? ({'/'.join(DRINK_CONFIG.keys())}): "

    def render(self) -> str:
        decorator_map: frozendict[StrType, Callable] = frozendict(
            {  # pyrefly: ignore [bad-argument-count]
                StrType.INVALID_OPTION: DecoratorType.PRINT_IN_RED(),
                StrType.REQUEST_ORDER: DecoratorType.COLORIZE_IN_GREEN(),
            }
        )
        decorator: Callable | None = decorator_map.get(self)

        def val_func():
            return self.value

        return decorator(val_func)() if decorator else self.value


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
    order_director = OrderDirector(order=user_choice)
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
        user_choice = get_prompt(
            message=StrType.REQUEST_ORDER.render(), target_type=str
        )
        if handler := options.get(user_choice):
            handler()
            continue

        if user_choice not in DRINK_CONFIG:
            StrType.INVALID_OPTION.render()

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
