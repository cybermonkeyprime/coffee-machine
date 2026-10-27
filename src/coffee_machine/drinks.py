from dataclasses import dataclass
from enum import StrEnum, auto

from .ingredients import Ingredients
from .money.price import Price
from .style.decorator_type import DecoratorType


@dataclass(frozen=True, slots=True)
class ItemSpecs:
    name: str
    ingredients: Ingredients
    price: Price

    @DecoratorType.PRINT_IN_WHITE()
    def item_info(self) -> str:
        return f"{self.name.title()}: ${self.price.amount:.2f}"


class DrinkType(StrEnum):
    ESPRESSO = auto()
    LATTE = auto()
    CAPPUCCINO = auto()


DRINK_CONFIG = frozendict(  # pyright: ignore[reportUndefinedVariable]
    {
        DrinkType.ESPRESSO: ItemSpecs(
            DrinkType.ESPRESSO,
            Ingredients(water=50, coffee=18),
            Price(1.5),
        ),
        DrinkType.LATTE: ItemSpecs(
            DrinkType.LATTE,
            Ingredients(water=200, milk=150, coffee=24),
            Price(2.5),
        ),
        DrinkType.CAPPUCCINO: ItemSpecs(
            DrinkType.CAPPUCCINO,
            Ingredients(water=250, milk=100, coffee=24),
            Price(3.0),
        ),
    }
)
