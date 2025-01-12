from src.types.products import Products
from src.utils.hybrid_search import HybridSearch
import json
import ast
from src.utils.image_handler import load_image


def get_unique_categories(payloads:Products):
    return set(payload.category_name for payload in payloads)


def search(query:str, search_function:HybridSearch)->str:
    results = search_function.hybrid_search(query)
    return json.dumps([product.images[0] for product in results])

def show_images(image_links:str):
    """Use this function to parse and show images of products.

        Args:
            image_links (str): urls to images
        """
    image_links = ast.literal_eval(image_links)
    [load_image(i).show() for i in image_links]
    return "images shown successfully"


# if __name__ == "__main__":
#     print(show_images(image_links="white shoe,asdf"))