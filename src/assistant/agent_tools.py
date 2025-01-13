from src.utils.hybrid_search import HybridSearch
import json


def search(query: str, num_image_search: int = 3, num_keyword_search: int = 3,
           search_function: HybridSearch = None) -> str:
    results = search_function.hybrid_search(query, qdrant_limit=num_image_search, mieli_limit=num_keyword_search)
    return json.dumps({"image_search": [product.images[0] for product in results.qdrant_products],
                       "keyword_search": [product.images[0] for product in results.mieli_products]})
