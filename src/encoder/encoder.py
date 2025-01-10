from fastembed import TextEmbedding, ImageEmbedding


class Encoder:
    def __init__(self):
        self.text_model_name = "Qdrant/clip-ViT-B-32-text"
        self.text_model = TextEmbedding(model_name=self.text_model_name)
        self.text_embeddings_size = self.text_model._get_model_description(self.text_model_name)[
            "dim"]  # dimension of text embeddings, produced by CLIP text encoder (512)

        self.image_model_name = "Qdrant/clip-ViT-B-32-vision"  # CLIP image encoder
        self.image_model = ImageEmbedding(model_name=self.image_model_name)
        self.image_embeddings_size = self.image_model._get_model_description(self.image_model_name)[
            "dim"]  # dimension of image embeddings, produced by CLIP image encoder (512)

    def embed_text(self, text):
        return list(self.text_model.embed(text)).pop()

    def embed_image(self, image):
        return list(self.image_model.embed(image)).pop()

if __name__ == "__main__":
    encoder = Encoder()
    print(encoder.embed_text("hello world"))
