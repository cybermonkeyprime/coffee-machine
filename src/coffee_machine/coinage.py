from enum import Enum

from rich.console import Console

from .style.decorator_type import DecoratorType


class CoinageType(Enum):
    PENNIES = 0.01
    NICKELS = 0.05
    DIMES = 0.10
    QUARTERS = 0.25
    DOLLARS = 1.00

    @classmethod
    def valid_items(cls):
        return tuple(member.name for member in cls)

    @DecoratorType.INPUT_IN_YELLOW.value
    def get_input_request(self):
        return f"How many {self.name.title()}? "

    def request_amount(self):
        console = Console()
        return int(console.input(self.get_input_request()) or 0) * self.value

    @classmethod
    def insert_coins(cls) -> tuple:
        return tuple(member.request_amount() for member in cls)


def process_coins() -> float:
    """Returns the total calculated for coins inserted."""
    output_coinage_request()
    total = sum(CoinageType.insert_coins())
    print()  # add newline
    if total > 0:
        output_total(total)
    return total


@DecoratorType.PRINT_IN_GREEN.value
def output_coinage_request() -> str:
    return "Please insert coins."


@DecoratorType.PRINT_IN_GREEN.value
def output_total(total: float) -> str:
    return f"You inserted ${total:.2f}"
