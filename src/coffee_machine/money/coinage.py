from dataclasses import dataclass
from enum import StrEnum, auto

from ..prompt import get_prompt
from ..style.decorator_type import DecoratorType


class CoinType(StrEnum):
    PENNIES = auto()
    NICKELS = auto()
    DIMES = auto()
    QUARTERS = auto()
    DOLLARS = auto()


@dataclass(frozen=True, slots=True)
class Denomination:
    coin_type: CoinType
    value: float

    @DecoratorType.INPUT_IN_YELLOW()
    def get_input_request(self):
        return f"How many {self.coin_type.title()}? "

    def get_coin_type(self):
        quantity = get_prompt(self.get_input_request(), int)
        return CoinCount(COIN_CONFIG[self.coin_type], quantity).total_value


COIN_CONFIG: dict[CoinType, Denomination] = frozendict(  # pyright: ignore[reportUndefinedVariable]
    {
        CoinType.PENNIES: Denomination(CoinType.PENNIES, 0.01),
        CoinType.NICKELS: Denomination(CoinType.NICKELS, 0.05),
        CoinType.DIMES: Denomination(CoinType.DIMES, 0.10),
        CoinType.QUARTERS: Denomination(CoinType.QUARTERS, 0.25),
        CoinType.DOLLARS: Denomination(CoinType.DOLLARS, 1.00),
    }
)


@dataclass(frozen=True, slots=True)
class CoinCount:
    denomination: Denomination
    quantity: int

    @property
    def total_value(self) -> float:
        return self.quantity * self.denomination.value


def calculate_total_inserted() -> float:
    total = sum(
        denomination.get_coin_type() for denomination in COIN_CONFIG.values()
    )
    return 0 if total < 0 else total


@DecoratorType.PRINT_IN_GREEN()
def request_coinage() -> str:
    return "Please insert coins."


def main():
    calculate_total_inserted()


if __name__ == "__main__":
    main()
