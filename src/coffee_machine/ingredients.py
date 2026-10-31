from collections.abc import Iterator, Mapping
from dataclasses import dataclass
from enum import StrEnum


class UnitType(StrEnum):
    LIQUID = "ml"
    SOLID = "g"


@dataclass(frozen=True, slots=True, kw_only=True)
class Ingredients(Mapping[str, int]):
    water: int = 0
    milk: int = 0
    coffee: int = 0

    def __getitem__(self, key: str) -> int:
        # Crucial: This allows dictionary-style lookup: obj['a']
        if key not in self.__dataclass_fields__:
            raise KeyError(key)
        return getattr(self, key)

    def __iter__(self) -> Iterator:
        # Crucial: This allows looping and dict conversion
        return iter(self.__dataclass_fields__)

    def __len__(self) -> int:
        return len(self.__dataclass_fields__)

    @classmethod
    def get_units(cls, key) -> UnitType:
        return UnitType.SOLID if key == "coffee" else UnitType.LIQUID
