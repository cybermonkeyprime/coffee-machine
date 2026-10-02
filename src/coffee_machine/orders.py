from dataclasses import dataclass

from .coinage import process_coins
from .order_data import MENU, Ingredients, ItemSpecs
from .resources import RESOURCES, ResourceValidator
from .style import decorator
from .style.rich_colors import RichColors
from .transactions import TransactionHandler

task_decorator = decorator.StylizedIndentPrinter(
    style=RichColors.TASK, end="\n", use_output=True
)


@dataclass(frozen=True, slots=False)
class OrderMaker:
    order: str

    @property
    def order_ingredients(self) -> Ingredients:
        return MENU[self.order].ingredients

    def execute(self):
        tasks = ("deduct_ingredients", "give_order")
        for task in tasks:
            getattr(self, task)()

    def deduct_ingredients(self) -> None:
        """Deduct the required ingredients from the resources."""
        for item, amount in self.order_ingredients.items():
            RESOURCES[item] -= amount

    @task_decorator
    def add_ingredient(self, ingredient: str):

        return f" Adding {ingredient} - {self.order_ingredients[ingredient]}"

    def simulate_order_processing(self):
        for ingredient in self.order_ingredients:
            self.add_ingredient(ingredient)

    @task_decorator
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
            print(f"{self.order.title()}: ${self.drink_cost:.2f}")
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

    @task_decorator
    def fetch_order_info(self):
        return f"{self.order.title()}: ${self.drink_cost:.2f}"
