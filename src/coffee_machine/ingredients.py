from collections.abc import Mapping
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Ingredients(Mapping[str, int]):
    water: int = 0
    milk: int = 0
    coffee: int = 0

    def __getitem__(self, key: str) -> int:
        # Crucial: This allows dictionary-style lookup: obj['a']
        if key not in self.__dataclass_fields__:
            raise KeyError(key)
        return getattr(self, key)

    def __iter__(self):
        # Crucial: This allows looping and dict conversion
        return iter(self.__dataclass_fields__)

    def __len__(self):
        return len(self.__dataclass_fields__)


@dataclass(frozen=True, slots=True)
class ItemSpecs:
    ingredients: Ingredients
    cost: Cost


@dataclass(frozen=True, slots=True)
class Cost:
    amount: float


MENU: dict[str, ItemSpecs] = {
    "espresso": ItemSpecs(Ingredients(water=50, coffee=18), Cost(1.5)),
    "latte": ItemSpecs(Ingredients(water=200, milk=150, coffee=24), Cost(2.5)),
    "cappuccino": ItemSpecs(
        Ingredients(water=250, milk=100, coffee=24), Cost(3.0)
    ),
}
