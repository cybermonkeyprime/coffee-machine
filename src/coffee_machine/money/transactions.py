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
        get_cash_collected(self.money_received)
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
def get_cash_collected(change: float):
    return f"Cash collected is ${change:.2f}"


@DecoratorType.PRINT_IN_GREEN()
def has_change_message(change: float):
    return f"Your Change is ${change:.2f}"


@DecoratorType.PRINT_PADDED_RED()
def transaction_failure_message() -> str:
    return "Sorry! That's not enough money. Money refunded."
