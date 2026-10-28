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
        Price(1.5),
    )
    LATTE = ItemSpec(
        Ingredients(water=200, milk=150, coffee=24),
        Price(2.5),
    )
    CAPPUCCINO = ItemSpec(
        Ingredients(water=250, milk=100, coffee=24),
        Price(3.0),
    )

    @DecoratorType.PRINT_IN_WHITE()
    def item_price(self) -> str:
        return f"{self.name.title()}: ${self.value.price.amount:.2f}"


DRINK_CONFIG = frozendict(  # pyright: ignore[reportUndefinedVariable]
    {member.name.lower(): member.value for member in DrinkType}
)


def run() -> None:
    for drink in DrinkType:
        drink.item_price()


if __name__ == "__main__":
    run()
