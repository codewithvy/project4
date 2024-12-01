from pydantic import BaseModel

# Product Model
class Product(BaseModel):
    id: int = None
    name: str
    description: str
    price: float
    inventory: int
    category_id: int

# Category Model
class Category(BaseModel):
    id: int = None
    name: str
