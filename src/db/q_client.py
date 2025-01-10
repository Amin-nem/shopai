from qdrant_client import QdrantClient, models
from src.encoder.encoder import Encoder
from src.utils.load_json_data import load_json_data
from src.utils.image_handler import load_image
from src.utils.build_filters import build_filters

QDRANT_PATH = "./quadrant"  # This is for local storage
QDRANT_COLLECTION_NAME = "text_image"


class QClient:
    def __init__(self):
        self.client = QdrantClient(path=QDRANT_PATH)
        self.encoder = Encoder()
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
        else:
            self.client.update_collection(
                collection_name=QDRANT_COLLECTION_NAME,
                vectors_config={
                    "image": models.VectorParams(size=self.encoder.image_embeddings_size,
                                                 distance=models.Distance.COSINE),
                    "text": models.VectorParams(size=self.encoder.text_embeddings_size,
                                                distance=models.Distance.COSINE),
                }
            )

    def add_to_quadrant(self, datapoint):
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

    def batch_add_to_quadrant(self, datapoints):
        for datapoint in datapoints:
            self.add_to_quadrant(datapoint)

    def query_images_with_text(self, query="", n=1, category_names=None, price_low=None, price_high=None):
        filters = build_filters(category_names=category_names, price_low=price_low, price_high=price_high)["qdrant_filters"]
        # encode text
        encoded_query = self.encoder.embed_text(query)
        # search
        res = self.client.search(
            collection_name=QDRANT_COLLECTION_NAME,
            query_vector=("image", encoded_query),
            with_payload=True,
            limit=n,
            query_filter=models.Filter(
                must=filters,
            )
        )
        res = [i.payload["id"] for i in res]
        return res


if __name__ == "__main__":
    data = load_json_data()[300:350]
    client = QClient()
    for i in data:
        if not i.current_price is None:
            client.add_to_quadrant(i)

    # client.batch_add_to_quadrant(data)
    print(client.client.count(collection_name=QDRANT_COLLECTION_NAME))
    print(client.client.get_fastembed_vector_params())

    print(client.query_images_with_text("blue shirt", 3, price_low=0, price_high=200000 ))
    client.client.close()
