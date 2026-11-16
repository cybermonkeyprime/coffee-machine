from collections.abc import Iterator, Mapping
from dataclasses import dataclass
from enum import StrEnum, auto

from .style.decorator_type import DecoratorType


class ResourceType(StrEnum):
    WATER = auto()
    MILK = auto()
    COFFEE = auto()
    MOCHA = auto()
    CREAM = auto()


@dataclass(slots=True, kw_only=True)
class ResourceBase(Mapping[str, int]):
    water: int = 0
    milk: int = 0
    coffee: int = 0
    mocha: int = 0
    cream: int = 0


@dataclass(slots=True, kw_only=True)
class Resources(ResourceBase):
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

    def __iter__(self) -> Iterator:
        return iter(self.__dataclass_fields__)

    def __len__(self) -> int:
        return len(self.__dataclass_fields__)

    @DecoratorType.PRINT_IN_YELLOW()
    def get_resource_info(self, key: str) -> str:
        from .ingredients import Ingredients, UnitType

        unit: UnitType = Ingredients.get_units(key)

        base_output: str = f"{key.title()}: {getattr(self, key)}"

        return base_output if unit == UnitType.VOID else f"{base_output}{unit}"

    def get_all_info(self) -> None:
        for key in self:
            self.get_resource_info(key)
        print()


RESOURCES = Resources(water=300, milk=200, coffee=100, mocha=20, cream=8)


@dataclass(frozen=True, slots=True)
class ResourceValidator:
    ingredients: ResourceBase

    @property
    def valid_resource_keys(self) -> tuple:
        return tuple(key.title() for key in RESOURCES)

    def validate_all(self) -> bool:
        return all(
            self.validate_resource(name=key, quantity=value)
            for key, value in self.ingredients.items()
        )

    def validate_resource(self, *, name: str, quantity: int) -> bool:

        if (titlized_name := name.title()) not in self.valid_resource_keys:
            self.on_error(
                f"{titlized_name} not found in {self.valid_resource_keys}"
            )
            return False

        if quantity > RESOURCES.get(name.lower(), 0):
            self.on_error(f"Sorry, there is not enough {titlized_name}.")
            return False

        return True

    @DecoratorType.PRINT_IN_RED()
    def on_error(self, *, message):
        return message
