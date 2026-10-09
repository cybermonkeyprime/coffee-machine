from dataclasses import dataclass

from .style import decorator
from .style.rich_colors import RichColors

task_decorator = decorator.StylizedIndentPrinter(
    style=RichColors.YELLOW, indent=1, use_output=True, end="\n"
)


@dataclass(slots=True)
class TransactionHandler:
    money_received: float
    item_cost: float

    def execute(self) -> bool:
        """Returns true when the payment is accepted or false if insufficient."""
        if self.money_received < self.item_cost:
            self.transaction_failure_message()
            return False
        self.has_change()
        return True

    def has_change(self):
        change = self.calculate_change()
        if change > 0:
            self.has_change_message(change)

    def calculate_change(self) -> float:
        return round(self.money_received - self.item_cost, 2)

    @task_decorator
    def has_change_message(self, change: float):
        return f"Your change is ${change:.2f}\n"

    def transaction_failure(self):
        return self.money_received < self.item_cost

    @task_decorator
    def transaction_failure_message(self) -> str:
        return "Sorry! That's not enough money. Money refunded."
