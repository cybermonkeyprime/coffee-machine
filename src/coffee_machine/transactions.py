from dataclasses import dataclass

from .style.decorator_type import DecoratorType


@dataclass(slots=True)
class TransactionHandler:
    money_received: float
    item_cost: float

    def execute(self) -> bool:
        """Returns true when the payment is accepted or false if insufficient."""
        if self.money_received < self.item_cost:
            self.transaction_failure_message()
            return False
        print()
        self.has_change()
        return True

    def has_change(self):
        if (change := self.calculate_change()) > 0:
            self.has_change_message(change)

    def calculate_change(self) -> float:
        return round(self.money_received - self.item_cost, 2)

    @DecoratorType.PRINT_IN_GREEN()
    def has_change_message(self, change: float):
        return f"Your change is ${change:.2f}\n"

    def transaction_failure(self):
        return self.money_received < self.item_cost

    @DecoratorType.PRINT_PADDED_RED()
    def transaction_failure_message(self) -> str:
        return "Sorry! That's not enough money. Money refunded."
