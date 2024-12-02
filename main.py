from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from database import engine, SessionLocal
from models import Base, Product, Category
from pydantic import BaseModel
from fastapi import Depends, HTTPException
from database import get_db
from ShoppingCart_ import ShoppingCart




# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Shopping Cart Routes
@app.post("/cart/add")
def add_to_cart(product_id: int, quantity: int, db: Session = Depends(get_db)):
    cart = ShoppingCart(db)
    try:
        cart.add_item(product_id, quantity)
        return {"message": "Item added to cart", "cart": cart.get_items()}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/cart/remove/{product_id}")
def remove_from_cart(product_id: int, db: Session = Depends(get_db)):
    cart = ShoppingCart(db)
    cart.remove_item(product_id)
    return {"message": "Item removed from cart", "cart": cart.get_items()}

@app.put("/cart/update/{product_id}")
def update_cart_quantity(product_id: int, quantity: int, db: Session = Depends(get_db)):
    cart = ShoppingCart(db)
    try:
        cart.update_quantity(product_id, quantity)
        return {"message": "Cart updated", "cart": cart.get_items()}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/cart/total")
def get_cart_total(db: Session = Depends(get_db)):
    cart = ShoppingCart(db)
    total = cart.get_total()
    return {"total": total}


# Pydantic schemas for input/output
class ProductSchema(BaseModel):
    id: int
    name: str
    description: str
    price: float
    inventory: int
    category_id: int

    class Config:
        orm_mode = True


class CategorySchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


# Create the database tables
Base.metadata.create_all(bind=engine)

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()

# CRUD for Products
@app.post("/products/", response_model=ProductSchema)
def create_product(product: ProductSchema, db: Session = Depends(get_db)):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@app.get("/products/", response_model=List[ProductSchema])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


@app.get("/products/{product_id}", response_model=ProductSchema)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.put("/products/{product_id}", response_model=ProductSchema)
def update_product(product_id: int, updated_product: ProductSchema, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in updated_product.dict().items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product


@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"message": "Product deleted"}


# CRUD for Categories
@app.post("/categories/", response_model=CategorySchema)
def create_category(category: CategorySchema, db: Session = Depends(get_db)):
    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@app.get("/categories/", response_model=List[CategorySchema])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()
