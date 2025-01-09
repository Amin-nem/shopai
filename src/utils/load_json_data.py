import json
from src.utils.product_model import Products

JSON_PATH = "../../products_1.json"

def load_json_data():
    with open(JSON_PATH,"r") as f:
        d = json.load(f)
    return Products.validate_python(d)



if __name__ == "__main__":
    data = load_json_data()
    print(data[0])