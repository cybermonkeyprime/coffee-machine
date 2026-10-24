from .drinks import DrinkType, ItemSpecs

MENU: dict[str, ItemSpecs] = DrinkType.as_dict()

MENU_ITEMS = tuple(drink_name for drink_name in MENU)
