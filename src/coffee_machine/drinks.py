from dataclasses import dataclass
from decimal import Decimal
from enum import Enum

from .cursor_ctrl import move_cursor_up
from .ingredients import Ingredients, UnitType
from .style.decorator_type import DecoratorType


@dataclass(frozen=True, slots=True, kw_only=True)
class ItemSpec:
    ingredients: Ingredients
    price: Decimal


class DrinkType(Enum):
    ESPRESSO = ItemSpec(
        ingredients=Ingredients(water=50, coffee=18),
        price=Decimal(value="1.5"),
    )
    LATTE = ItemSpec(
        ingredients=Ingredients(water=200, milk=150, coffee=24),
        price=Decimal(value="2.5"),
    )
    CAPPUCCINO = ItemSpec(
        ingredients=Ingredients(water=250, milk=100, coffee=24),
        price=Decimal(value="3.0"),
    )
    COCOA = ItemSpec(
        ingredients=Ingredients(milk=100, mocha=2, cream=1),
        price=Decimal(value="1.0"),
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
        return f" {unit}s" if unit == UnitType.PUMP else unit

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
            self.render_wo_description()
            if self.unit == UnitType.VOID
            else self.render_w_description()
        )

    def render_w_description(self) -> str:
        return (
            f"Adding {self.valid_ingredient_amount}{self.unit} "
            f"of {self.ingredient_name}"
        )

    def render_wo_description(self) -> str:
        return f"Adding {self.ingredient_name}"


def get_valid_ingredient_amount(drink, ingredient) -> int:
    item_ingredients: Ingredients = get_drink_ingredients(drink=drink)
    return item_ingredients.get(ingredient) or 0


def get_drink_ingredients(*, drink: str) -> Ingredients:

    if drink not in DRINK_CONFIG:
        raise KeyError(f"{drink} not in DRINK_CONFIG")

    return DRINK_CONFIG[drink].ingredients


@DecoratorType.PRINT_IN_WHITE()
def drink_price(drink: DrinkType) -> str:
    return f"{drink.name.title()}: ${drink.value.price:.2f}"


def run() -> None:
    for drink in DrinkType:
        drink_price(drink)


if __name__ == "__main__":
    run()
