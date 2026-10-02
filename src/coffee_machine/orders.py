from dataclasses import dataclass

from .order_data import MENU, Ingredients
from .resources import RESOURCES
from .style import decorator
from .style.rich_colors import RichColors

task_decorator = decorator.StylizedIndentPrinter(
    style=RichColors.TASK, end="\n", use_output=True
)


@dataclass(frozen=True, slots=True)
class OrderMaker:
    order: str

    @property
    def order_ingredients(self) -> Ingredients:
        return MENU[self.order].ingredients

    def execute(self):
        tasks = ("deduct_ingredients", "response")
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
    def response(self) -> str:
        return f"Here is your {self.order.title()}☕"
