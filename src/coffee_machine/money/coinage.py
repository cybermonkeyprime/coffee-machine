from dataclasses import dataclass
from enum import Enum

from ..prompt import get_prompt
from ..style.decorator_type import DecoratorType


@dataclass(frozen=True, slots=True)
class Denomination:
    coin_type: CoinType
    price: float


@dataclass(frozen=True, slots=True)
class CoinCount:
    denomination: Denomination
    quantity: int

    @property
    def total_value(self) -> float:
        return self.quantity * self.denomination.price


class CoinType(Enum):
    PENNIES = 0.01
    NICKELS = 0.05
    DIMES = 0.10
    QUARTERS = 0.25
    DOLLARS = 1.00

    def get_denomination(self) -> Denomination:
        return Denomination(coin_type=self, price=self.value)

    @DecoratorType.INPUT_IN_YELLOW()
    def get_input_request(self) -> str:
        return f"How many {self.name.title()}? "

    def get_coin_quantity(self) -> int:
        return get_prompt(message=self.get_input_request(), target_type=int)

    def get_coin_type(self):
        quantity = self.get_coin_quantity()
        return CoinCount(self.get_denomination(), quantity).total_value


COIN_CONFIG: frozendict[str, Denomination] = frozendict(  # pyright: ignore[reportUndefinedVariable]
    {member.name.lower(): member.get_denomination() for member in CoinType}  # pyrefly: ignore[bad-argument-count]
)


def calculate_total_inserted() -> float:
    total: float = sum(member.get_coin_type() for member in CoinType)
    return 0 if total < 0 else total


@DecoratorType.PRINT_IN_GREEN()
def request_coinage() -> str:
    return "Please insert coins."


def main():
    calculate_total_inserted()


if __name__ == "__main__":
    main()
