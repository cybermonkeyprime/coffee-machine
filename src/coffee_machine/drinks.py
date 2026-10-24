from dataclasses import dataclass
from enum import Enum

from .ingredients import Ingredients
from .money.price import Price
from .style.decorator_type import DecoratorType


@dataclass(frozen=True, slots=True)
class ItemSpecs:
    ingredients: Ingredients
    price: Price


class DrinkType(Enum):
    ESPRESSO = ItemSpecs(Ingredients(water=50, coffee=18), Price(1.5))
    LATTE = ItemSpecs(Ingredients(water=200, milk=150, coffee=24), Price(2.5))
    CAPPUCCINO = ItemSpecs(
        Ingredients(water=250, milk=100, coffee=24), Price(3.0)
    )

    @classmethod
    def as_dict(cls):
        return {member.name.lower(): member.value for member in cls}

    @classmethod
    @DecoratorType.PRINT_IN_WHITE()
    def item_info(cls, name: str) -> str:
        member = cls[name.upper()]
        return f"{member.name.title()}:  ${member.value.price.amount:.2f}"
