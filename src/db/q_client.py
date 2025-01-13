import logging
from qdrant_client import QdrantClient, models
from src.encoder.encoder import Encoder
from src.utils.image_handler import load_image
from src.utils.build_filters import build_filters
from src.types.products import Product, Products
from typing import List, Optional

logging.basicConfig(
    level=logging.INFO,  # Set minimum log level
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

QDRANT_COLLECTION_NAME = "text_image"


class QClient:
    def __init__(self, qdrantclient: QdrantClient, encoder: Encoder) -> None:
        self.client = qdrantclient
        self.encoder = encoder

        if not self.client.collection_exists(QDRANT_COLLECTION_NAME):
            self.client.create_collection(
                collection_name=QDRANT_COLLECTION_NAME,
                vectors_config={
                    "image": models.VectorParams(
                        size=self.encoder.image_embeddings_size,
                        distance=models.Distance.COSINE
                    ),
                    "text": models.VectorParams(
                        size=self.encoder.text_embeddings_size,
                        distance=models.Distance.COSINE
                    ),
                }
            )
            logger.info("Created collection %s", QDRANT_COLLECTION_NAME)
        else:
            logger.info("Collection %s already exists", QDRANT_COLLECTION_NAME)

    def add_to_qdrant(self, datapoint: Product) -> None:
        image_vector = self.encoder.embed_image(load_image(datapoint.images[0]))
        text_vector = self.encoder.embed_text(datapoint.name)

        self.client.upload_points(
            collection_name=QDRANT_COLLECTION_NAME,
            points=[
                models.PointStruct(
                    id=datapoint.id,
                    vector={
                        "text": text_vector,
                        "image": image_vector,
                    },
                    payload=datapoint.model_dump(),
                )
            ],
        )

    def batch_add_to_qdrant(self, datapoints: Products) -> None:
        for datapoint in datapoints:
            try:
                self.add_to_qdrant(datapoint)
            # not that important to load all the images
            except:
                pass

    def query_images_with_text(
            self,
            query: str = "",
            limit: int = 1,
            category_names: Optional[List[str]] = None,
            price_low: int = 0,
            price_high: int = 0,
    ) -> Products:
        if category_names is None:
            category_names = []

        filters = build_filters(
            category_names=category_names,
            price_low=price_low,
            price_high=price_high
        ).qdrant_filters

        encoded_query = self.encoder.embed_text(query)

        res = self.client.search(
            collection_name=QDRANT_COLLECTION_NAME,
            query_vector=("image", encoded_query),
            with_payload=True,
            limit=limit,
            query_filter=models.Filter(must=filters),
        )

        logger.info(
            "Query for '%s' returned %d results from Qdrant",
            query, len(res)
        )

        return Products.validate_python([hit.payload for hit in res])
