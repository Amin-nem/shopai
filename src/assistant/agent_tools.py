from itertools import product

from src.types import products
from src.utils.hybrid_search import HybridSearch
import json
# import ast
# from src.utils.image_handler import load_image


def search(query:str,num_image_search: int = 3, num_keyword_search: int = 3, search_function:HybridSearch=None)->str:
    results = search_function.hybrid_search(query, qdrant_limit=num_image_search,mieli_limit=num_keyword_search)
    return json.dumps({"image_search":[product.images[0] for product in results.qdrant_products],
     "keyword_search":[product.images[0] for product in results.mieli_products]})

# def show_images(image_links:str):
#     """Use this function to parse and show images of products.
#
#         Args:
#             image_links (str): urls to images
#         """
#     image_links = ast.literal_eval(image_links)
#     [load_image(i).show() for i in image_links]
#     return "images shown successfully"


# if __name__ == "__main__":
#     print(show_images(image_links="white shoe,asdf"))