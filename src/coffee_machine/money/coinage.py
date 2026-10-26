from dataclasses import dataclass
from enum import Enum

from ..prompt import get_prompt
from ..style.decorator_type import DecoratorType


class CoinType(Enum):
    PENNIES = 0.01
    NICKELS = 0.05
    DIMES = 0.10
    QUARTERS = 0.25
    DOLLARS = 1.00

    @property
    def denomination(self):
        return Denomination(name=self.name, value=self.value)

    @classmethod
    def valid_items(cls):
        return tuple(member.name for member in cls)

    @classmethod
    def insert_coins(cls) -> tuple:
        request_coinage()
        return tuple(member.denomination.request_amount() for member in cls)

    @classmethod
    def get_total_coinage(cls) -> int:
        total = sum(cls.insert_coins())
        return 0 if total < 0 else total


@dataclass(frozen=True, slots=True)
class Denomination:
    name: str
    value: float

    @DecoratorType.INPUT_IN_YELLOW()
    def get_input_request(self):
        return f"How many {self.name.title()}? "

    def request_amount(self):
        count = get_prompt(self.get_input_request(), int)
        return count * self.value


@DecoratorType.PRINT_IN_GREEN()
def request_coinage() -> str:
    return "Please insert coins."


def main():
    pass


if __name__ == "__main__":
    main()
