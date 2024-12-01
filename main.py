from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
from models import Product, Category

app = FastAPI()

# In-memory storage for products and categories
products = []
categories = []

# CRUD for Products
@app.post("/products/", response_model=Product)
def create_product(product: Product):
    product.id = len(products) + 1
    products.append(product)
    return product

@app.get("/products/", response_model=List[Product])
def get_products():
    return products

@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    for product in products:
        if product.id == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")

@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, updated_product: Product):
    for index, product in enumerate(products):
        if product.id == product_id:
            updated_product.id = product_id
            products[index] = updated_product
            return updated_product
    raise HTTPException(status_code=404, detail="Product not found")

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    global products
    products = [product for product in products if product.id != product_id]
    return {"message": "Product deleted"}

# Search Products
@app.get("/products/search/", response_model=List[Product])
def search_products(query: str = Query(...)):
    return [product for product in products if query.lower() in product.name.lower()]

# CRUD for Categories
@app.post("/categories/", response_model=Category)
def create_category(category: Category):
    category.id = len(categories) + 1
    categories.append(category)
    return category

@app.get("/categories/", response_model=List[Category])
def get_categories():
    return categories
