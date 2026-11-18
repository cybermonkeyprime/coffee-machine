from dataclasses import dataclass
from enum import StrEnum, auto

from .resources import ResourceBase, ResourceType


class UnitType(StrEnum):
    LIQUID = "ml"
    GROUND = "g"
    PUMP = auto()
    VOID = auto()


@dataclass(init=False, slots=True, kw_only=True)
class Ingredients(ResourceBase):
    @classmethod
    def get_units(cls, key) -> UnitType:
        unit_map: frozendict[ResourceType, UnitType] = frozendict(
            {  # pyrefly: ignore[bad-argument-count]
                ResourceType.COFFEE: UnitType.GROUND,
                ResourceType.MOCHA: UnitType.PUMP,
                ResourceType.CREAM: UnitType.VOID,
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
