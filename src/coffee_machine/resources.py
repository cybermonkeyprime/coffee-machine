from collections.abc import Iterator, Mapping
from dataclasses import dataclass, field
from enum import StrEnum, auto

from .style.decorator_type import DecoratorType


class ResourceType(StrEnum):
    WATER = auto()
    MILK = auto()
    COFFEE = auto()
    MOCHA = auto()
    CREAM = auto()


@dataclass(init=False, kw_only=True)
class ResourceBase(Mapping[str, int]):
    _resources: dict[str, int] = field(
        default_factory=lambda: {
            resource.value: 0 for resource in ResourceType
        }
    )

    def __init__(self, **kwargs: int) -> None:
        self._resources = {resource.value: 0 for resource in ResourceType}

        for key, value in kwargs.items():
            self[key] = value

    def __setitem__(self, key: str, value: int) -> None:
        if key not in self._resources:
            raise KeyError(f"'{key}' is not a valid field")

        if not isinstance(value, int):
            raise TypeError(
                f"Value for '{key}' must be an int, got {type(value).__name__}"
            )

        self._resources[key] = value

    def __getitem__(self, key: str) -> int:
        if key not in self._resources:
            raise KeyError(key)

        return self._resources[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self._resources)

    def __len__(self) -> int:
        return len(self._resources)


@dataclass(init=False, slots=True, kw_only=True)
class Resources(ResourceBase):
    @DecoratorType.PRINT_IN_YELLOW()
    def get_resource_info(self, key: str) -> str:
        from .ingredients import Ingredients, UnitType

        unit: UnitType = Ingredients.get_units(key)

        base_output: str = f"{key.title()}: {self[key]}"

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
