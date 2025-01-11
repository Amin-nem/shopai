from meilisearch import Client
from src.utils.load_json_data import load_json_data
from src.utils.build_filters import build_filters
from src.types.products import Product, Products
from typing import List

MEILI_HOST = "aSampleMasterKey"
MEILI_URL = "http://localhost:7700"
MEILI_INDEX = "image-text"


class Mclient:
    def __init__(self):
        self.client = Client(url=MEILI_URL, api_key=MEILI_HOST)
        self.client.index(MEILI_INDEX).update_filterable_attributes(
            ["category_name",
             "current_price", ]
        )
        self.client.index(MEILI_INDEX).update_searchable_attributes(
            ["name",
             "description", ]
        )

    def add_to_meili(self, datapoint:Product):
        self.client.index(MEILI_INDEX).add_documents(datapoint.model_dump())

    def batch_add_to_meili(self, datapoints:Products):
        for datapoint in datapoints:
            self.add_to_meili(datapoint)

    def search(self, query:str, limit:int=2,category_names:List[str]=[], price_low:int=0, price_high:int=0)->Products:
        filters = build_filters(category_names=category_names, price_low=price_low, price_high=price_high).meili_filters

        res = self.client.index(MEILI_INDEX).search(query=query, opt_params={"filter": filters, "limit": limit})
        return Products.validate_python(res.get("hits"))


if __name__ == "__main__":
    data = load_json_data()[1100:2000]
    client = Mclient()
    # print(data[0].model_dump())
    client.batch_add_to_meili([i for i in data if not i.current_price is None])

    print(client.client.get_all_stats())

    print(client.search("long", limit=7, category_names=["shirts"], price_low=100))
