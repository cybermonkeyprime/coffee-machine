from dataclasses import dataclass

from .coinage import process_coins
from .order_data import MENU, Ingredients, ItemSpecs
from .resources import RESOURCES, ResourceValidator
from .style.decorator_type import DecoratorType
from .transactions import TransactionHandler


@dataclass(frozen=True, slots=False)
class OrderMaker:
    order: str

    @property
    def order_ingredients(self) -> Ingredients:
        return MENU[self.order].ingredients

    def execute(self):
        tasks = ("deduct_ingredients", "order_prep", "give_order")
        for task in tasks:
            getattr(self, task)()

    def deduct_ingredients(self) -> None:
        """Deduct the required ingredients from the resources."""
        for item, amount in self.order_ingredients.items():
            RESOURCES[item] -= amount

    @DecoratorType.PRINT_IN_YELLOW()
    def add_ingredient(self, ingredient: str):
        unit = Ingredients.get_units(ingredient)
        return f"Adding {self.order_ingredients[ingredient]}{unit} of {ingredient}"

    def order_prep(self):
        tasks = ("prep_msg", "add_ingredients", "blend_order", "heat_order")
        for task in tasks:
            callback = getattr(self, task)
            callback()

    @DecoratorType.PRINT_PADDED_YELLOW()
    def prep_msg(self):
        return "Preparing your order ..."

    def add_ingredients(self) -> None:
        for ingredient in self.order_ingredients:
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
        return f"Here is your {self.order.title()}☕"


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
        return self.drink_info.cost.amount

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
