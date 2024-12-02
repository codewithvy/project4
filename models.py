from pydantic import BaseModel
from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class CartItem(Base):
    __tablename__ = "cart_items"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    # Relationship to the Product model
    product = relationship("Product")


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

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)