from qdrant_client import QdrantClient, models
from src.encoder.encoder import Encoder
from src.utils.load_json_data import load_json_data
from src.utils.image_handler import load_image
from src.utils.build_filters import build_filters
from src.types.products import Product, Products
from typing import List

# Define the path to the Qdrant database folder in a cross-platform way
QDRANT_COLLECTION_NAME = "text_image"


class QClient:
    def __init__(self,qdrantclient: QdrantClient, encoder: Encoder):
        self.client = qdrantclient
        self.encoder = encoder
        if not self.client.collection_exists(QDRANT_COLLECTION_NAME):
            self.client.create_collection(
                collection_name=QDRANT_COLLECTION_NAME,
                vectors_config={
                    "image": models.VectorParams(size=self.encoder.image_embeddings_size,
                                                 distance=models.Distance.COSINE),
                    "text": models.VectorParams(size=self.encoder.text_embeddings_size,
                                                distance=models.Distance.COSINE),
                }
            )
            print("Created collection {}".format(QDRANT_COLLECTION_NAME))
        # else:
        #     self.client.update_collection(
        #         collection_name=QDRANT_COLLECTION_NAME,
        #         vectors_config={
        #             "image": models.VectorParams(size=self.encoder.image_embeddings_size,
        #                                          distance=models.Distance.COSINE),
        #             "text": models.VectorParams(size=self.encoder.text_embeddings_size,
        #                                         distance=models.Distance.COSINE),
        #         }
        #     )
        #     print("Updated collection {}".format(QDRANT_COLLECTION_NAME))

    def add_to_quadrant(self, datapoint: Product):
        self.client.upload_points(
            collection_name=QDRANT_COLLECTION_NAME,
            points=[
                models.PointStruct(
                    id=datapoint.id,
                    vector={
                        "text": self.encoder.embed_text(datapoint.name),
                        "image": self.encoder.embed_image(load_image(datapoint.images[0]))
                    },
                    payload=datapoint.model_dump(),
                )
            ]
        )

    def batch_add_to_quadrant(self, datapoints: Products):
        for datapoint in datapoints:
            self.add_to_quadrant(datapoint)

    def query_images_with_text(self, query: str = "", limit: int = 1, category_names: List[str] = [],
                               price_low: int = 0, price_high: int = 0) -> Products:
        # build filters
        filters = build_filters(category_names=category_names, price_low=price_low,
                                price_high=price_high).qdrant_filters
        # encode text
        encoded_query = self.encoder.embed_text(query)
        # search
        res = self.client.search(
            collection_name=QDRANT_COLLECTION_NAME,
            query_vector=("image", encoded_query),
            with_payload=True,
            limit=limit,
            query_filter=models.Filter(
                must=filters,
            )
        )
        # convert to Products type
        res = Products.validate_python([i.payload for i in res])
        return res


if __name__ == "__main__":
    qdrant_connection = QdrantClient(url="http://localhost",port=6333)
    encoder = Encoder()
    data = load_json_data()[0:5]
    client = QClient(qdrantclient=qdrant_connection,encoder=encoder)
    for i in data:
        if not i.current_price is None:
            client.add_to_quadrant(i)

    # client.batch_add_to_quadrant(data)
    print(client.client.count(collection_name=QDRANT_COLLECTION_NAME))
    print(client.client.get_fastembed_vector_params())

    print(client.query_images_with_text("white", limit=3))
    client.client.close()
