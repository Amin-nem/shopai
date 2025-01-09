from PIL import Image
import requests
from io import BytesIO


def load_image(url):
    response = requests.get(url)
    response.raise_for_status()  # Ensure the request was successful
    loaded_image = Image.open(BytesIO(response.content))
    return loaded_image

# if __name__ == '__main__':
#     image = load_image("https://media.6media.me/media/catalog/product/cache/51d09e6ba6f1fb68e23a90a2eb71ff17/b/k/bkk19056_sage_xl_1.jpg")
#     image.show()
