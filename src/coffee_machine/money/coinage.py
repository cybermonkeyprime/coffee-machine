from dataclasses import dataclass
from enum import Enum

from ..prompt import get_prompt
from ..style.decorator_type import DecoratorType


@dataclass(frozen=True, slots=True, kw_only=True)
class Denomination:
    coin_type: CoinType
    price: float

    @DecoratorType.INPUT_IN_YELLOW()
    def get_input_request(self) -> str:
        return f"How many {self.coin_type.name.title()}? "

    def get_quantity(self) -> int:
        return get_prompt(message=self.get_input_request(), target_type=int)

    def get_total_value(self) -> float:
        quantity: int = self.get_quantity()
        return CoinCount(denomination=self, quantity=quantity).total_value


@dataclass(frozen=True, slots=True, kw_only=True)
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

    @property
    def denomination(self) -> Denomination:
        return Denomination(coin_type=self, price=self.value)


COIN_CONFIG: frozendict[str, Denomination] = frozendict(
    {  # pyrefly: ignore[bad-argument-count]
        member.name.lower(): member.denomination for member in CoinType
    }
)


def calculate_total_inserted() -> float:
    total: float = sum(
        member.denomination.get_total_value() for member in CoinType
    )
    return 0 if total < 0 else total


@DecoratorType.PRINT_IN_WHITE()
def request_coinage() -> str:
    return "Please insert coins or bills:"


def main() -> None:
    calculate_total_inserted()


if __name__ == "__main__":
    main()
