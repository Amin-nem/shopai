import logging
from typing import List, Optional

from meilisearch import Client

# from src.utils.load_json_data import load_json_data
from src.utils.build_filters import build_filters
from src.types.products import Product, Products

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)

DEFAULT_MEILI_API_KEY = "aSampleMasterKey"
DEFAULT_MEILI_URL = "http://localhost:7700"
DEFAULT_MEILI_INDEX = "image-text"


class MeiliClient:

    def __init__(
        self,
        url: str = DEFAULT_MEILI_URL,
        api_key: str = DEFAULT_MEILI_API_KEY,
        index_name: str = DEFAULT_MEILI_INDEX,
    ) -> None:

        self.url = url
        self.api_key = api_key
        self.index_name = index_name
        self.client = Client(url=self.url, api_key=self.api_key)

        self.client.index(self.index_name).update_filterable_attributes(
            ["category_name", "current_price"]
        )
        self.client.index(self.index_name).update_searchable_attributes(
            ["name", "description"]
        )
        logger.info("Initialized MeiliClient for index '%s'", self.index_name)

    def add_to_meili(self, datapoint: Product) -> None:
        doc = datapoint.model_dump()
        self.client.index(self.index_name).add_documents([doc])

    def batch_add_to_meili(self, datapoints: Products) -> None:
        for datapoint in datapoints:
            self.add_to_meili(datapoint)

    def search(
        self,
        query: str,
        limit: int = 2,
        category_names: Optional[List[str]] = None,
        price_low: int = 0,
        price_high: int = 0,
    ) -> Products:
        if category_names is None:
            category_names = []

        filters = build_filters(
            category_names=category_names,
            price_low=price_low,
            price_high=price_high,
        ).meili_filters

        logger.info(
            "Performing search on index '%s' with query: '%s' | limit: %d | filters: %s",
            self.index_name, query, limit, filters
        )

        response = self.client.index(self.index_name).search(
            query=query,
            opt_params={
                "filter": filters,
                "limit": limit
            }
        )

        hits = response.get("hits", [])
        logger.debug("Received %d hits from Meilisearch", len(hits))

        return Products.validate_python(hits)


# if __name__ == "__main__":
#     data = load_json_data()[1100:2000]
#
#     client = MeiliClient()
#     valid_data = [item for item in data if item.current_price is not None]
#     client.batch_add_to_meili(valid_data)
#
#     stats = client.client.get_all_stats()
#
#     results = client.search(
#         "long",
#         limit=7,
#         category_names=["shirts"],
#         price_low=100
#     )
