from pydantic import BaseModel, TypeAdapter


class Product(BaseModel):
    id: int
    name: str
    description: str
    images: list[str]
    category_name: str | None = None
    link: str | None = None
    currency: str
    current_price: float | None = None


Products = TypeAdapter(list[Product])