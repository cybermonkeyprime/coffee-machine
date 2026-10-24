from dataclasses import dataclass

from ..style.decorator_type import DecoratorType


@dataclass(slots=True)
class TransactionHandler:
    money_received: float
    item_cost: float

    def execute(self) -> bool:
        """
        Returns true when the payment is accepted or false if insufficient.
        """
        if self.on_transaction_failure():
            transaction_failure_message()
            return False
        print()
        self.has_change()
        return True

    def has_change(self):
        if (change := self.calculate_change()) > 0:
            has_change_message(change)

    def calculate_change(self) -> float:
        return round(self.money_received - self.item_cost, 2)

    def on_transaction_failure(self):
        return self.money_received < self.item_cost


@DecoratorType.PRINT_IN_GREEN()
def has_change_message(change: float):
    return f"Your change is ${change:.2f}\n"


@DecoratorType.PRINT_PADDED_RED()
def transaction_failure_message() -> str:
    return "Sorry! That's not enough money. Money refunded."
