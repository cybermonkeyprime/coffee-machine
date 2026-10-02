#!/usr/bin/env python
from dataclasses import dataclass

from rich.console import Console

from .coinage import process_coins
from .exception.decorator.abort_decorator import AbortDecorator
from .ingredients import MENU, Ingredients
from .orders import OrderMaker
from .resources import RESOURCES, ResourceValidator
from .style import decorator
from .style.decorator.figletizer import FontType
from .style.rich_colors import RichColors
from .transactions import TransactionHandler

task_decorator = decorator.ColorizedIndentPrinter(style="Warning", indent=1)


MENU_ITEMS = tuple(drink_name for drink_name in MENU)


@decorator.Colorizer(style=RichColors.TASK)
def user_input():
    return f"What would you like? ({'/'.join(MENU_ITEMS)}): "


@decorator.StyledFigletPrinter(
    font=FontType.SLANT, use_output=True, style=RichColors.VARIABLE
)
def get_title():
    return "JavaGenie"


@dataclass
class CoffeeMachine:
    is_on: bool = True
    profit: float = 0.0
    # resources: dict = field(default_factory=lambda: RESOURCES)

    def process_drink_order(self, user_choice: str):
        drink = MENU.get(user_choice)
        if drink and self.is_resource_sufficient(drink.ingredients):
            print(f"{user_choice.title()}: ${drink.cost.amount:.2f}")
            payment = process_coins()
            transaction = TransactionHandler(payment, drink.cost.amount)
            if transaction.execute():
                self.profit += drink.cost.amount
                OrderMaker(user_choice).execute()

    def is_resource_sufficient(self, order_ingredients: Ingredients) -> bool:
        """Check if resources are sufficient for the order."""
        return ResourceValidator(order_ingredients).validate()

    @AbortDecorator()
    def execute(self) -> None:
        """Main function to run the coffee machine."""
        console = Console()
        while self.is_on:
            user_choice = console.input(user_input())
            options = {
                "quit": turn_off,
                "report": get_report,
            }
            if handler := options.get(user_choice):
                handler()
                continue
            self.process_drink_order(user_choice)


@task_decorator
def turn_off(self):
    self.is_on = False
    return "Thank you!"


@task_decorator
def get_item_info(self, key: str) -> str:
    unit = "g" if key == "coffee" else "ml"
    return f"{key.title()}: {RESOURCES[key]}{unit}"


@task_decorator
def get_report(self):
    for key in RESOURCES:
        self.get_item_info(key)
    return f"Money: ${self.profit:.2f}"


def run():
    get_title()
    CoffeeMachine().execute()


if __name__ == "__main__":
    run()
