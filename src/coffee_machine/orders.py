from dataclasses import dataclass

from .drinks import DRINK_CONFIG, ItemSpec
from .ingredients import (
    IngredientRenderer,
    Ingredients,
)
from .money.coinage import calculate_total_inserted, request_coinage
from .money.transactions import TransactionHandler
from .resources import RESOURCES, ResourceValidator
from .style.decorator_type import DecoratorType


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

    @DecoratorType.PRINT_PADDED_YELLOW()
    def prep_msg(self) -> str:
        return "Preparing your order ..."

    def add_ingredients(self) -> None:
        IngredientRenderer(drink=self.item_name).render_all()

    @DecoratorType.PRINT_PADDED_YELLOW()
    def blend_order(self) -> str:
        return "Blendng it all together ..."

    @DecoratorType.PRINT_IN_YELLOW()
    def heat_order(self) -> str:
        return "Heating to 96°C ...\n"

    @DecoratorType.PRINT_IN_YELLOW()
    def give_order(self) -> str:
        return f"Here is your {self.item_name.title()}☕"

    def preparation(self) -> None:
        steps = ("prep_msg", "add_ingredients", "blend_order", "heat_order")
        self.order_pipeline(steps)

    def execute(self) -> None:
        steps = ("deduct_ingredients", "preparation", "give_order")
        self.order_pipeline(steps)

    def order_pipeline(self, steps: tuple) -> None:
        for step in steps:
            callback: str | None = getattr(self, step)
            if callable(callback):
                callback()


@dataclass(slots=True)
class OrderDirector:
    order: str
    profit: float = 0.0

    @property
    def drink_info(self) -> ItemSpec:
        return DRINK_CONFIG[self.order]

    @property
    def drink_ingredients(self) -> Ingredients:
        return self.drink_info.ingredients

    @property
    def drink_cost(self) -> float:
        return self.drink_info.price.amount

    def process_order(self) -> None:
        if not self.is_valid_order():
            return

        if not self.execute_transaction():
            return

        self.profit += self.drink_cost

        OrderMaker(item_name=self.order).execute()

    def execute_transaction(self) -> bool:
        request_coinage()
        return TransactionHandler(
            money_received=calculate_total_inserted(),
            item_cost=self.drink_cost,
        ).execute()

    def is_valid_order(self) -> ItemSpec | bool:
        return (
            self.drink_info
            and ResourceValidator(self.drink_ingredients).validate()
        )
