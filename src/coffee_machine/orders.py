from dataclasses import dataclass

from .ingredients import MENU, Ingredients
from .resources import RESOURCES
from .style import decorator
from .style.rich_colors import RichColors


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

    @decorator.StylizedIndentPrinter(
        style=RichColors.TASK, end="\n", use_output=True
    )
    def response(self) -> str:
        return f"Here is your {self.order.title()}☕"
