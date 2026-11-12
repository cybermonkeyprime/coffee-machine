from collections.abc import Callable
from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum

from .drinks import DRINK_CONFIG, ItemSpec
from .ingredients import (
    IngredientRenderer,
    Ingredients,
)
from .money.coinage import calculate_total_inserted, request_coinage
from .money.transactions import TransactionHandler
from .resources import RESOURCES, ResourceValidator
from .style.decorator_type import DecoratorType


class PrepStep(StrEnum):
    PREP_MSG = "Preparing your order ..."
    BLEND_ORDER = "Blendng it all together ..."
    HEAT_ORDER = "Heating to 96°C ..."

    @DecoratorType.PRINT_PADDED_YELLOW()
    def render(self) -> str:
        return self.value


@dataclass(frozen=True, slots=False)
class OrderMaker:
    item_name: str

    @property
    def item_ingredients(self) -> Ingredients:
        return DRINK_CONFIG[self.item_name].ingredients

    def deduct_ingredients(self) -> None:
        """Deduct the required ingredients from the resources."""
        for item, amount in self.item_ingredients.items():
            RESOURCES[item] -= amount

    def add_ingredients(self) -> None:
        IngredientRenderer(drink=self.item_name).render_all()

    @DecoratorType.PRINT_IN_YELLOW()
    def give_order(self) -> str:
        return f"Here is your {self.item_name.title()}!☕"

    def preparation(self) -> None:
        steps: tuple[Callable, ...] = (
            PrepStep.PREP_MSG.render,
            self.add_ingredients,
            PrepStep.BLEND_ORDER.render,
            PrepStep.HEAT_ORDER.render,
        )
        self.preparation_pipeline(steps=steps)

    def execute(self) -> None:
        steps = ("deduct_ingredients", "preparation", "give_order")
        self.getattr_pipeline(steps)

    def getattr_pipeline(self, steps: tuple) -> None:
        for step in steps:
            callback: str | None = getattr(self, step)
            if callable(callback):
                callback()
        print()

    def preparation_pipeline(self, steps: tuple) -> None:
        for step in steps:
            if callable(step):
                step()


@dataclass(slots=True)
class OrderDirector:
    order: str
    profit: Decimal = Decimal(value="0")

    @property
    def drink_info(self) -> ItemSpec:
        return DRINK_CONFIG[self.order]

    @property
    def drink_ingredients(self) -> Ingredients:
        return self.drink_info.ingredients

    @property
    def drink_cost(self) -> Decimal:
        return Decimal(value=self.drink_info.price)

    def order_rules(self) -> ItemSpec | bool:
        return self.validate_order() and self.execute_transaction()

    def process_order(self) -> None:

        if not self.order_rules():
            return

        self.profit += Decimal(value=self.drink_cost)

        OrderMaker(item_name=self.order).execute()

    def execute_transaction(self) -> bool:
        request_coinage()
        return TransactionHandler(
            money_received=calculate_total_inserted(),
            item_cost=self.drink_cost,
        ).execute()

    def validate_order(self) -> ItemSpec | bool:
        return (
            self.drink_info
            and ResourceValidator(self.drink_ingredients).validate_all()
        )
