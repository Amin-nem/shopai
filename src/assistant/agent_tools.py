from src.db.meili_client import Mclient
from src.types.products import Product, Products
from typing import List
import json


mclient = Mclient()

def get_unique_categories(payloads:Products):
    return set(payload.category_name for payload in payloads)


def write_query():
    pass


def search(query:str):
    """Use this function to search for products.

        Args:
            query (str): keyword to search for.

        Returns:
            List: top results as a list of dicts.
        """
    return json.dumps([product.model_dump() for product in mclient.search(query)])


if __name__ == "__main__":
    print(search("white shoe"))