from collections.abc import Mapping
from dataclasses import dataclass

from .order_data import Ingredients
from .style import decorator
from .style.rich_colors import RichColors

task_decorator = decorator.ColorizedIndentPrinter(
    style=RichColors.YELLOW, indent=1
)


@dataclass(slots=True)
class Resources(Mapping[str, int]):
    water: int = 0
    milk: int = 0
    coffee: int = 0

    def __setitem__(self, key: str, value: int) -> None:
        if key not in self.__dataclass_fields__:
            raise KeyError(f"'{key}' is not a valid field")
        if not isinstance(value, int):
            raise TypeError(
                f"Value for '{key}' must be an int, got {type(value).__name__}"
            )
        setattr(self, key, value)

    def __getitem__(self, key: str) -> int:
        if key not in self.__dataclass_fields__:
            raise KeyError(key)
        return getattr(self, key)

    def __iter__(self):
        return iter(self.__dataclass_fields__)

    def __len__(self):
        return len(self.__dataclass_fields__)

    @task_decorator
    def get_info(self, key: str) -> str:
        unit = Ingredients.get_units(key)
        return f"{key.title()}: {getattr(self, key)}{unit}"

    def get_all_info(self):
        for key in self:
            self.get_info(key)


RESOURCES = Resources(water=300, milk=200, coffee=100)


@dataclass(frozen=True, slots=True)
class ResourceValidator:
    order_ingredients: Ingredients

    def validate(self) -> bool:
        for item, amount in self.order_ingredients.items():
            if amount > RESOURCES[item]:
                self.error_response(item)
                return False
        return True

    @task_decorator
    def error_response(self, item):
        return f"Sorry, there is not enough {item}."
