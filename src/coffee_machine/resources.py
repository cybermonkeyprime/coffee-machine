from collections.abc import Iterator, Mapping
from dataclasses import dataclass

from .style.decorator_type import DecoratorType


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
        error_pipeline: list[tuple[bool, KeyError | TypeError]] = [
            self.on_missing_key(key),
            self.on_invalid_type(key, value),
        ]
        for error, response in iter(error_pipeline):
            if error:
                raise response

        setattr(self, key, value)

    def on_missing_key(self, key: str) -> tuple[bool, KeyError]:
        return (
            key not in self.__dataclass_fields__,
            KeyError(f"'{key}' is not a valid field"),
        )

    def on_invalid_type(self, key: str, value: int) -> tuple[bool, TypeError]:
        return (
            not isinstance(value, int),
            TypeError(
                f"Value for '{key}' must be an int, got {type(value).__name__}"
            ),
        )

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
        pipeline: list[tuple[bool, str]] = [
            self.on_missing_resource_name(name),
            self.on_insufficient_resource(name, quantity),
        ]
        for error, response in iter(pipeline):
            if error:
                self.on_error(message=response)
                return False
        return True

    def on_missing_resource_name(self, name: str) -> tuple[bool, str]:
        titlized_name: str = name.title()
        return (
            titlized_name not in self.valid_resource_keys,
            f"{titlized_name} not found in {self.valid_resource_keys}",
        )

    def on_insufficient_resource(
        self, name: str, quantity: int
    ) -> tuple[bool, str]:
        return (
            quantity > RESOURCES.get(name, 0),
            f"Sorry, there is not enough {name.title()}.",
        )

    @DecoratorType.PRINT_IN_RED()
    def on_error(self, *, message):
        return message
