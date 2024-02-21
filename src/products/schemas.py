from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):

    name: str
    description: str
    price: int


class Product(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int


class ProductUpdatePartial(Product):

    name: str | None = None
    description: str | None = None
    price: int | None = None