"""
Water Street menu category normalization.
Maps raw category strings to canonical SAGCO category names.
"""

# Canonical category mapping
CATEGORY_MAP = {
    # Sunday Brunch variants
    "sunday brunch": "SUNDAY_BRUNCH",
    "brunch": "SUNDAY_BRUNCH",
    "sunday": "SUNDAY_BRUNCH",
    # Oyster Bar
    "oyster": "OYSTER_BAR",
    "oyster bar": "OYSTER_BAR",
    "raw bar": "OYSTER_BAR",
    "oysters": "OYSTER_BAR",
    # Sushi
    "sushi": "SUSHI",
    "sushi roll": "SUSHI",
    "rolls": "SUSHI",
    "roll": "SUSHI",
    # Appetizers
    "appetizer": "APPETIZERS",
    "appetizers": "APPETIZERS",
    "starters": "APPETIZERS",
    "starter": "APPETIZERS",
    # Entrees
    "entree": "ENTREES",
    "entrees": "ENTREES",
    "main": "ENTREES",
    "mains": "ENTREES",
    "dinner": "ENTREES",
    # Desserts
    "dessert": "DESSERTS",
    "desserts": "DESSERTS",
    # Drinks
    "drink": "DRINKS",
    "drinks": "DRINKS",
    "beverage": "DRINKS",
    "beverages": "DRINKS",
    "cocktail": "DRINKS",
    "cocktails": "DRINKS",
    "wine": "DRINKS",
    "beer": "DRINKS",
    # Soups / Salads
    "soup": "SOUPS_SALADS",
    "salad": "SOUPS_SALADS",
    "soups": "SOUPS_SALADS",
    "salads": "SOUPS_SALADS",
    "soups & salads": "SOUPS_SALADS",
    # Sides
    "side": "SIDES",
    "sides": "SIDES",
    "side dish": "SIDES",
}

CANONICAL_CATEGORIES = sorted(set(CATEGORY_MAP.values()))


def normalize_category(raw: str) -> str:
    """
    Normalize a raw category string to its canonical form.
    Returns 'UNKNOWN' if not recognized.
    """
    if not raw:
        return "UNKNOWN"
    key = raw.strip().lower()
    return CATEGORY_MAP.get(key, raw.strip().upper().replace(" ", "_"))


def normalize_rows(rows: list, category_field: str = "Category") -> list:
    """Normalize category field in all rows."""
    result = []
    for row in rows:
        new_row = dict(row)
        if category_field in new_row:
            new_row[category_field] = normalize_category(str(new_row[category_field]))
        result.append(new_row)
    return result


def group_by_category(rows: list, category_field: str = "Category") -> dict:
    """Group rows by (normalized) category."""
    groups: dict = {}
    for row in rows:
        cat = normalize_category(str(row.get(category_field, "UNKNOWN")))
        groups.setdefault(cat, []).append(row)
    return groups
