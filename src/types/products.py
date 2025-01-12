from pydantic import BaseModel, TypeAdapter


class Product(BaseModel):
    id: int
    name: str
    category_name: str | None = None
    description: str
    current_price: float | None = None
    link: str | None = None
    images: list[str]
    currency: str



Products = TypeAdapter(list[Product])


class HybridProducts(BaseModel):
    qdrant_products: list[Product]
    mieli_products: list[Product]
