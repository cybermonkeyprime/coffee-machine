from dataclasses import dataclass
from decimal import Decimal
from enum import Enum

from ..cursor_ctrl import move_cursor_up
from ..prompt import get_prompt
from ..style.decorator_type import DecoratorType


@dataclass(frozen=True, slots=True, kw_only=True)
class Denomination:
    coin_type: CoinType
    price: Decimal

    @DecoratorType.INPUT_IN_YELLOW()
    def get_input_request(self) -> str:
        return f"How many {self.coin_type.name.title()}? "

    def get_quantity(self) -> int:
        prompt = get_prompt(message=self.get_input_request(), target_type=int)
        if prompt == 0:
            print(move_cursor_up())
        return prompt

    def get_total_value(self) -> Decimal:
        quantity: int = self.get_quantity()
        return CoinCount(denomination=self, quantity=quantity).total_value


@dataclass(frozen=True, slots=True, kw_only=True)
class CoinCount:
    denomination: Denomination
    quantity: int

    @property
    def total_value(self) -> Decimal:
        return self.quantity * self.denomination.price


class CoinType(Enum):
    PENNIES = Decimal(value="0.01")
    NICKELS = Decimal(value="0.05")
    DIMES = Decimal(value="0.10")
    QUARTERS = Decimal(value="0.25")
    DOLLARS = Decimal(value="1.00")

    @property
    def denomination(self) -> Denomination:
        return Denomination(coin_type=self, price=self.value)


COIN_CONFIG: frozendict[str, Denomination] = frozendict(
    {  # pyrefly: ignore[bad-argument-count]
        member.name.lower(): member.denomination for member in CoinType
    }
)


def calculate_total_inserted() -> Decimal:

    total: Decimal = sum(
        (member.denomination.get_total_value() for member in CoinType),
        start=Decimal(value="0"),
    )
    return max(total, Decimal(value="0"))


@DecoratorType.PRINT_IN_WHITE()
def request_coinage() -> str:
    return "Please insert coins or bills:"


def main() -> None:
    calculate_total_inserted()


if __name__ == "__main__":
    main()
