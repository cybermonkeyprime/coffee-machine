#!/usr/bin/env python
from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum

from .drinks import DRINK_CONFIG, DrinkType, ItemSpec, drink_price
from .exception.decorator.abort_decorator import AbortDecorator
from .ingredients import IngredientRenderer
from .orders import OrderDirector
from .prompt import get_prompt
from .resources import RESOURCES
from .style.decorator_type import DecoratorType
from .versioning.version_config import SoftwareVersion


@dataclass(slots=True, kw_only=True)
class Status:
    is_on: bool
    profit: float


class StrType(StrEnum):
    INVALID_OPTION = "Please select a valid option."
    REQUEST_ORDER = "What would you like? "
    # ({'/'.join(DRINK_CONFIG.keys())}): "

    def render(self) -> str:
        decorator_map: frozendict[StrType, Callable] = frozendict(
            {  # pyrefly: ignore [bad-argument-count]
                StrType.INVALID_OPTION: DecoratorType.PRINT_IN_RED(),
                StrType.REQUEST_ORDER: DecoratorType.COLORIZE_IN_GREEN(),
            }
        )
        decorator: Callable | None = decorator_map.get(self)

        def val_func() -> str:
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


def drink_menu() -> None:
    for drink in DRINK_CONFIG:
        MenuRenderer(drink).drink_info()


@dataclass(frozen=True, slots=True)
class MenuRenderer:
    drink: str
    data: frozendict[str, ItemSpec] = DRINK_CONFIG

    @property
    def drink_name(self) -> str:
        return self.drink.title()

    @property
    def drink_price(self) -> str:
        price: float = DRINK_CONFIG[self.drink].price.amount
        return f"${price:.2f}"

    @DecoratorType.PRINT_IN_YELLOW()
    def drink_info(self) -> str:
        return f"{self.drink_name:<12} {self.drink_price:>7}"


@AbortDecorator()
def coffee_machine() -> None:
    """Main function to run the coffee machine."""
    options: dict[str, Callable] = {
        "quit": turn_off,
        "report": get_report,
    }
    while STATUS.is_on:
        user_choice: str = get_prompt(
            message=StrType.REQUEST_ORDER.render(), target_type=str
        ).lower()
        if handler := options.get(user_choice):
            handler()
            continue

        if user_choice not in DRINK_CONFIG:
            StrType.INVALID_OPTION.render()

        if user_choice in DRINK_CONFIG:
            drink_price(DrinkType[user_choice.upper()])
            process_drink_order(user_choice)


def run() -> None:
    steps: tuple[Callable, ...] = (
        SoftwareVersion.header,
        drink_menu,
        coffee_machine,
    )

    for step in steps:
        if callable(step):
            step()


if __name__ == "__main__":
    run()
