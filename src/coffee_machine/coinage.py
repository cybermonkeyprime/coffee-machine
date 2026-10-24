from dataclasses import dataclass
from enum import Enum

from .prompt import get_prompt
from .style.decorator_type import DecoratorType


class CoinageType(Enum):
    PENNIES = 0.01
    NICKELS = 0.05
    DIMES = 0.10
    QUARTERS = 0.25
    DOLLARS = 1.00

    @property
    def coinage(self):
        return CoinageCollector(name=self.name, value=self.value)

    @classmethod
    def valid_items(cls):
        return tuple(member.name for member in cls)

    @classmethod
    @DecoratorType.PRINT_IN_GREEN()
    def coinage_request(cls) -> str:
        return "Please insert coins."

    @classmethod
    def insert_coins(cls) -> tuple:
        cls.coinage_request()
        return tuple(member.coinage.request_amount() for member in cls)

    @classmethod
    def get_total_coinage(cls) -> int:
        return sum(cls.insert_coins())


@dataclass(frozen=True, slots=True)
class CoinageCollector:
    name: str
    value: float

    @DecoratorType.INPUT_IN_YELLOW()
    def get_input_request(self):
        return f"How many {self.name.title()}? "

    def request_amount(self):
        count = get_prompt(self.get_input_request(), int)
        return count * self.value


def process_coins() -> float:
    """Returns the total calculated for coins inserted."""
    sub_total = CoinageType.get_total_coinage()
    return 0 if sub_total < 0 else sub_total
