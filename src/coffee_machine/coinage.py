from enum import Enum

from .prompt import get_prompt
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

    @DecoratorType.INPUT_IN_YELLOW()
    def get_input_request(self):
        return f"How many {self.name.title()}? "

    def request_amount(self):
        count = get_prompt(self.get_input_request(), int)
        return count * self.value

    @classmethod
    def insert_coins(cls) -> tuple:
        return tuple(member.request_amount() for member in cls)


@DecoratorType.PRINT_IN_RED()
def invalid_int_response() -> str:
    return "Invalid input! Please enter a whole number."


def process_coins() -> float:
    """Returns the total calculated for coins inserted."""
    output_coinage_request()
    sub_total = sum(CoinageType.insert_coins())
    return 0 if sub_total < 0 else sub_total


@DecoratorType.PRINT_IN_GREEN()
def output_coinage_request() -> str:
    return "Please insert coins."


@DecoratorType.PRINT_IN_GREEN()
def output_total(total: float) -> str:
    return f"You inserted ${total:.2f}"
