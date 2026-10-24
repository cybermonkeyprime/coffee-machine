from dataclasses import dataclass

from .drinks import ItemSpecs
from .ingredients import Ingredients
from .menu import MENU
from .money.coinage import process_coins
from .money.transactions import TransactionHandler
from .resources import RESOURCES, ResourceValidator
from .style.decorator_type import DecoratorType


@dataclass(frozen=True, slots=False)
class OrderMaker:
    item_name: str

    @property
    def item_ingredients(self) -> Ingredients:
        return MENU[self.item_name].ingredients

    def deduct_ingredients(self) -> None:
        """Deduct the required ingredients from the resources."""
        for item, amount in self.item_ingredients.items():
            RESOURCES[item] -= amount

    @DecoratorType.PRINT_IN_YELLOW()
    def add_ingredient(self, ingredient: str):
        unit = Ingredients.get_units(ingredient)
        return (
            f"Adding {self.item_ingredients[ingredient]}{unit} of {ingredient}"
        )

    @DecoratorType.PRINT_PADDED_YELLOW()
    def prep_msg(self):
        return "Preparing your order ..."

    def add_ingredients(self) -> None:
        for ingredient in self.item_ingredients:
            self.add_ingredient(ingredient)
        print()

    @DecoratorType.PRINT_PADDED_YELLOW()
    def blend_order(self) -> str:
        return "Blendng it all together ..."

    @DecoratorType.PRINT_IN_YELLOW()
    def heat_order(self) -> str:
        return "Heating to 96°C ...\n"

    @DecoratorType.PRINT_IN_YELLOW()
    def give_order(self) -> str:
        return f"Here is your {self.item_name.title()}☕"

    def order_prep(self):
        tasks = ("prep_msg", "add_ingredients", "blend_order", "heat_order")
        for task in tasks:
            callback = getattr(self, task)
            callback()

    def execute(self):
        tasks = ("deduct_ingredients", "order_prep", "give_order")
        for task in tasks:
            getattr(self, task)()


@dataclass(slots=True)
class OrderDirector:
    order: str
    profit: float = 0.0

    @property
    def drink_info(self) -> ItemSpecs:
        return MENU[self.order]

    @property
    def drink_ingredients(self):
        return self.drink_info.ingredients

    @property
    def drink_cost(self):
        return self.drink_info.price.amount

    def process_order(self):
        if self.is_valid_order():
            payment = process_coins()
            transaction = TransactionHandler(payment, self.drink_cost)
            if transaction.execute():
                self.profit += self.drink_cost
                OrderMaker(self.order).execute()

    def is_valid_order(self):
        return (
            self.drink_info
            and ResourceValidator(self.drink_ingredients).validate()
        )

    @DecoratorType.PRINT_IN_YELLOW()
    def fetch_order_info(self):
        return f"{self.order.title()}: ${self.drink_cost:.2f}"
