from dataclasses import dataclass
from enum import Enum

from .ingredients import Ingredients
from .money.price import Price
from .style.decorator_type import DecoratorType


@dataclass(frozen=True, slots=True)
class ItemSpec:
    ingredients: Ingredients
    price: Price


class DrinkType(Enum):
    ESPRESSO = ItemSpec(
        Ingredients(water=50, coffee=18),
        Price(amount=1.5),
    )
    LATTE = ItemSpec(
        Ingredients(water=200, milk=150, coffee=24),
        Price(amount=2.5),
    )
    CAPPUCCINO = ItemSpec(
        Ingredients(water=250, milk=100, coffee=24),
        Price(amount=3.0),
    )


DRINK_CONFIG: frozendict[str, ItemSpec] = frozendict(  # pyright: ignore[reportUndefinedVariable]
    {member.name.lower(): member.value for member in DrinkType}  # pyrefly: ignore[bad-argument-count]
)


@DecoratorType.PRINT_IN_WHITE()
def drink_price(drink: DrinkType) -> str:
    return f"{drink.name.title()}: ${drink.value.price.amount:.2f}"


def run() -> None:
    for drink in DrinkType:
        drink_price(drink)


if __name__ == "__main__":
    run()
