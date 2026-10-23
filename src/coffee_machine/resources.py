from collections.abc import Mapping
from dataclasses import dataclass

from .order_data import Ingredients
from .style.decorator_type import DecoratorType


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

    @DecoratorType.PRINT_IN_YELLOW()
    def get_resource_info(self, key: str) -> str:
        unit = Ingredients.get_units(key)
        return f"{key.title()}: {getattr(self, key)}{unit}"

    def get_all_info(self):
        for key in self:
            self.get_resource_info(key)


RESOURCES = Resources(water=300, milk=200, coffee=100)


@dataclass(frozen=True, slots=True)
class ResourceValidator:
    ingredients: Ingredients

    def validate(self) -> bool:
        for item, amount in self.ingredients.items():
            if amount > RESOURCES[item]:
                self.on_resource_error(item)
                return False
        return True

    @DecoratorType.PRINT_IN_YELLOW()
    def on_resource_error(self, item):
        return f"Sorry, there is not enough {item}."
