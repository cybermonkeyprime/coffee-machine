from dataclasses import dataclass
from enum import Enum

from .ingredients import Ingredients, UnitType
from .money.price import Price
from .style.decorator_type import DecoratorType


@dataclass(frozen=True, slots=True, kw_only=True)
class ItemSpec:
    ingredients: Ingredients
    price: Price


class DrinkType(Enum):
    ESPRESSO = ItemSpec(
        ingredients=Ingredients(water=50, coffee=18),
        price=Price(amount=1.5),
    )
    LATTE = ItemSpec(
        ingredients=Ingredients(water=200, milk=150, coffee=24),
        price=Price(amount=2.5),
    )
    CAPPUCCINO = ItemSpec(
        ingredients=Ingredients(water=250, milk=100, coffee=24),
        price=Price(amount=3.0),
    )
    COCOA = ItemSpec(
        ingredients=Ingredients(milk=100, mocha=4, cream=1),
        price=Price(amount=1.5),
    )


DRINK_CONFIG: frozendict[str, ItemSpec] = frozendict(
    {member.name.lower(): member.value for member in DrinkType}  # pyrefly: ignore[bad-argument-count]
)


@dataclass(frozen=True, slots=True, kw_only=True)
class DrinkIngredientRenderer:
    from .style.decorator_type import DecoratorType

    drink: str
    ingredient: str

    @property
    def valid_amount(self) -> int:
        return get_valid_ingredient_amount(
            self.drink, ingredient=self.ingredient
        )

    @property
    def unit(self) -> str:
        unit: UnitType = Ingredients.get_units(key=self.ingredient)
        return f"{unit}s" if unit == UnitType.PUMP else unit

    def render_all(self) -> str:
        return move_cursor_up() if self.valid_amount <= 0 else self.render()

    @property
    def ingredient_name(self) -> str:
        return self.ingredient.replace("_", " ").title()

    @property
    def valid_ingredient_amount(self) -> int:
        return get_valid_ingredient_amount(
            self.drink, ingredient=self.ingredient
        )

    @DecoratorType.PRINT_IN_YELLOW()
    def render(self) -> str:
        return (
            f"Adding {self.valid_ingredient_amount}{self.unit} "
            f"of {self.ingredient_name}"
        )


def get_valid_ingredient_amount(drink, ingredient) -> int:

    item_ingredients: Ingredients = get_drink_ingredients(drink=drink)
    return item_ingredients.get(ingredient) or 0


def move_cursor_up() -> str:
    return "\033[A"


@DecoratorType.PRINT_IN_WHITE()
def drink_price(drink: DrinkType) -> str:
    return f"{drink.name.title()}: ${drink.value.price.amount:.2f}"


def get_drink_ingredients(*, drink: str) -> Ingredients:

    if drink not in DRINK_CONFIG:
        raise KeyError(f"{drink} not in DRINK_CONFIG")

    return DRINK_CONFIG[drink].ingredients


def run() -> None:
    for drink in DrinkType:
        drink_price(drink)


if __name__ == "__main__":
    run()
