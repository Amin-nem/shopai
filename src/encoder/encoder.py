from typing import List
from fastembed import TextEmbedding, ImageEmbedding
from src.types.encoder import ImageInput

TEXT_MODEL_NAME = "Qdrant/clip-ViT-B-32-text"
IMAGE_MODEL_NAME = "Qdrant/clip-ViT-B-32-vision"


class Encoder:

    def __init__(
            self,
            text_model_name: str = TEXT_MODEL_NAME,
            image_model_name: str = IMAGE_MODEL_NAME,
    ) -> None:
        self.text_model = TextEmbedding(model_name=text_model_name)
        self.image_model = ImageEmbedding(model_name=image_model_name)

        self.text_embeddings_size = self.text_model._get_model_description(text_model_name)["dim"]
        self.image_embeddings_size = self.image_model._get_model_description(image_model_name)["dim"]

    def embed_text(self, text: str) -> List[float]:
        embeddings = self.text_model.embed(text)
        embeddings_list = list(embeddings)
        return embeddings_list[0]

    def embed_image(self, image: ImageInput) -> List[float]:
        embeddings = self.image_model.embed(image)
        embeddings_list = list(embeddings)
        return embeddings_list[0]


if __name__ == "__main__":
    encoder = Encoder()
    print(encoder.embed_text("hello world"))
