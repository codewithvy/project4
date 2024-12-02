from sqlalchemy.orm import Session
from database import SessionLocal, Base, engine
from models import Product, Order
import sys

# Initialize the database
Base.metadata.create_all(bind=engine)

def fetch_products(db: Session):
    """Fetch all available products from the database."""
    products = db.query(Product).all()
    if not products:
        print("No products available!")
        return []
    print("\nAvailable Products:")
    print("-------------------")
    for product in products:
        print(f"ID: {product.id}, Name: {product.name}, Price: ${product.price}, Stock: {product.stock}")
    print("-------------------")
    return products

def add_product(db: Session):
    """Add a new product to the database."""
    name = input("Enter product name: ")
    description = input("Enter product description: ")
    price = float(input("Enter product price: "))
    stock = int(input("Enter product stock: "))

    product = Product(name=name, description=description, price=price, stock=stock)
    db.add(product)
    db.commit()
    print(f"Product '{name}' added successfully!")

def purchase_product(db: Session):
    """Purchase a product from the database."""
    product_id = int(input("Enter the product ID to purchase: "))
    quantity = int(input("Enter the quantity to purchase: "))

    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        print("Product not found!")
        return

    if product.stock < quantity:
        print(f"Insufficient stock! Only {product.stock} units available.")
        return

    total_price = product.price * quantity
    product.stock -= quantity

    # Create an order record
    order = Order(product_id=product_id, quantity=quantity, total_price=total_price, status="Purchased")
    db.add(order)
    db.commit()

    print(f"Purchase successful! Total Price: ${total_price:.2f}")
    print(f"Remaining stock for '{product.name}': {product.stock}")

def main():
    db = SessionLocal()
    try:
        while True:
            print("\n=== Interactive Shop ===")
            print("1. View Products")
            print("2. Add Product")
            print("3. Purchase Product")
            print("4. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                fetch_products(db)
            elif choice == "2":
                add_product(db)
            elif choice == "3":
                purchase_product(db)
            elif choice == "4":
                print("Exiting...")
                sys.exit()
            else:
                print("Invalid choice! Please try again.")
    finally:
        db.close()

if __name__ == "__main__":
    main()