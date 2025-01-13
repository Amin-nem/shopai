import json
from src.types.products import Products


def load_json_data(path: str) -> Products:
    with open(path, "r") as f:
        d = json.load(f)
    return Products.validate_python(d)
