from src.db.meili_client import Mclient
from src.types.products import Product, Products
from typing import List, Dict
from PIL import Image
import json


mclient = Mclient()

def get_unique_categories(payloads:Products):
    return set(payload.category_name for payload in payloads)


def write_query():
    pass


def search(query:str)->str:
    """Use this function to search for products.

        Args:
            query (str): keyword to search for.

        Returns:
            result List[str]: top results as a list of links.
        """
    results = mclient.search(query)
    return json.dumps([product.images[0] for product in results])

def show_images(image_links:List[str]):
    """Use this function to parse and show images of products.

        Args:
            image_links (str): urls to images
        """

    return [Image.open(i).show() for i in image_links]


if __name__ == "__main__":
    print(search("white shoe"))