from collections.abc import Callable
from dataclasses import dataclass

from .drinks import DRINK_CONFIG, ItemSpec
from .style.decorator_type import DecoratorType


@dataclass(frozen=True, slots=True, kw_only=True)
class MenuItemRenderer:
    drink: str
    specs: ItemSpec

    @property
    def drink_name(self) -> str:
        return self.drink.title()

    @property
    def drink_price(self) -> str:
        price: float = self.specs.price.amount
        return f"${price:.2f}"

    @DecoratorType.PRINT_IN_YELLOW()
    def drink_info(self) -> str:
        return f"{self.drink_name:<12} {self.drink_price:>7}"


@DecoratorType.PRINT_IN_WHITE()
def get_menu_title() -> str:
    return "Drink Menu"


def get_menu_items() -> None:
    for item, info in DRINK_CONFIG.items():
        MenuItemRenderer(drink=item, specs=info).drink_info()
    print()


def get_drink_menu() -> None:
    for step in MENU_STEPS:
        if callable(step):
            step()


MENU_STEPS: tuple[Callable, ...] = (get_menu_title, get_menu_items)


if __name__ == "__main__":
    get_drink_menu()
