from src.db.q_client import QClient
from src.db.meili_client import MeiliClient
from src.types.products import Products
from typing import List


class HybridSearch:
    def __init__(self,q_client: QClient,m_client: MeiliClient):
        self.q_client = q_client
        self.m_client = m_client

    def hybrid_search(self, query: str = "", qdrant_limit: int = 3, mieli_limit: int = 3,
                      category_names: List[str] = [],
                      price_low: int = 0, price_high: int = 0) -> Products:
        mieli_res = self.m_client.search(query, mieli_limit, category_names, price_low, price_high)
        qdrant_res = self.q_client.query_images_with_text(query, qdrant_limit, category_names, price_low, price_high)
        return qdrant_res + mieli_res


# if __name__ == "__main__":
#     q_client = QClient()
#     m_client = Mclient()
#     hybrid_search = HybridSearch(q_client, m_client)
#     res = hybrid_search.hybrid_search("white", qdrant_limit=1)
#     for i in res:
#         print(i)
