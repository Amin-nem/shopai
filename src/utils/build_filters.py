from qdrant_client import models
from typing import List
from src.types.filters import Filters


def build_filters(category_names: List[str] = [], price_low: int = 0, price_high: int = 0) -> Filters:
    meili_filters = ""
    if category_names:
        meili_filters += f"category_name IN [{', '.join(category_names)}]"
    if price_low:
        meili_filters += f"{' AND ' if category_names else ''}current_price >= {price_low}"
    if price_high:
        meili_filters += f" {' AND ' if category_names or price_low else ''}current_price <= {price_high}"

    qdrant_filters = []
    if category_names:
        qdrant_filters.append(models.FieldCondition(key="category_name", match=models.MatchAny(any=category_names)))
    if price_high or price_low:
        qdrant_filters.append(
            models.FieldCondition(key="current_price", range=models.Range(gte=price_low, lte=price_high)))
    return Filters(meili_filters=meili_filters, qdrant_filters=qdrant_filters)
