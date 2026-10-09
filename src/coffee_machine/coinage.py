from enum import Enum

from rich.console import Console

from .style import decorator
from .style.rich_colors import RichColors

task_decorator = decorator.StylizedIndentPrinter(
    style=RichColors.YELLOW, indent=1, use_output=False
)
print_task_decorator = decorator.StylizedIndentPrinter(
    style=RichColors.BOLD_GREEN, indent=1, use_output=True, end="\n\n"
)


class CoinageType(Enum):
    PENNIES = 0.01
    NICKELS = 0.05
    DIMES = 0.10
    QUARTERS = 0.25
    DOLLARS = 1.00

    @classmethod
    def valid_items(cls):
        return tuple(member.name for member in cls)

    @task_decorator
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
    if total > 0:
        output_total(total)
    return total


@print_task_decorator
def output_coinage_request() -> str:
    return "Please insert coins."


@print_task_decorator
def output_total(total: float) -> str:
    return f"You inserted ${total:.2f}"
