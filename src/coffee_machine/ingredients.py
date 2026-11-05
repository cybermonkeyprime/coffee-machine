from collections.abc import Iterator
from dataclasses import dataclass
from enum import StrEnum, auto

from .resources import ResourceBase


class UnitType(StrEnum):
    LIQUID = "ml"
    GROUND = "g"
    PUMPS = auto()
    VOID = auto()


@dataclass(slots=True, kw_only=True)
class Ingredients(ResourceBase):
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
        unit_map: frozendict[str, UnitType] = frozendict(
            {  # pyrefly: ignore[bad-argument-count]
                "coffee": UnitType.GROUND,
                "mocha": UnitType.PUMPS,
                "cream": UnitType.VOID,
            }
        )
        return unit_map.get(key, UnitType.LIQUID)


@dataclass(frozen=True, slots=True, kw_only=True)
class IngredientRenderer:
    drink: str

    @property
    def item_ingredients(self) -> Ingredients:
        from .drinks import get_drink_ingredients

        return get_drink_ingredients(drink=self.drink)

    def render_all(self) -> None:
        from .drinks import DrinkIngredientRenderer

        for ingredient in self.item_ingredients:
            DrinkIngredientRenderer(
                drink=self.drink, ingredient=ingredient
            ).render_all()
        print()
