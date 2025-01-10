from qdrant_client import models

def build_filters(category_names=None, price_low=None, price_high=None):
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
        qdrant_filters.append(models.FieldCondition(key="price", range=models.Range(gte=price_low, lte=price_high)))

    return {"qdrant_filters":qdrant_filters, "meili_filters":meili_filters}
