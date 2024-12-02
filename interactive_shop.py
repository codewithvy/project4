from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Product, Order, User
import bcrypt

# Initialize the database
from models import Base
Base.metadata.create_all(bind=engine)

# Utility functions for users
def register_user(db: Session):
    """Register a new user."""
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        print("User already exists!")
        return

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user = User(username=username, password=hashed_password)
    db.add(user)
    db.commit()
    print("User registered successfully!")

def login_user(db: Session):
    """Log in an existing user."""
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    user = db.query(User).filter(User.username == username).first()
    if not user:
        print("User does not exist!")
        return None

    if bcrypt.checkpw(password.encode('utf-8'), user.password):
        print(f"Welcome, {username}!")
        return user
    else:
        print("Invalid password!")
        return None

# Utility functions for products and orders
def fetch_products(db: Session):
    """Fetch all available products from the database."""
    products = db.query(Product).all()
    if not products:
        print("No products available!")
        return []

    print("\nAvailable Products:")
    print("-------------------")
    for product in products:
        print(f"ID: {product.id}, Name: {product.name}, Price: ${product.price:.2f}, Stock: {product.stock}")
    print("-------------------")
    return products

def purchase_product(db: Session, user: User):
    """Purchase a product from the database."""
    fetch_products(db)
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

# Main UI loop
def main():
    db = SessionLocal()
    current_user = None

    try:
        while True:
            if not current_user:
                print("\n=== Welcome to the E-Commerce Store ===")
                print("1. Register")
                print("2. Login")
                print("3. Exit")
                choice = input("Enter your choice: ")

                if choice == "1":
                    register_user(db)
                elif choice == "2":
                    current_user = login_user(db)
                elif choice == "3":
                    print("Thank you for visiting!")
                    break
                else:
                    print("Invalid choice. Please try again.")
            else:
                print("\n=== E-Commerce Menu ===")
                print("1. View Products")
                print("2. Purchase Product")
                print("3. Logout")
                print("4. Exit")
                choice = input("Enter your choice: ")

                if choice == "1":
                    fetch_products(db)
                elif choice == "2":
                    purchase_product(db, current_user)
                elif choice == "3":
                    print(f"Goodbye, {current_user.username}!")
                    current_user = None
                elif choice == "4":
                    print("Thank you for shopping!")
                    break
                else:
                    print("Invalid choice. Please try again.")
    finally:
        db.close()

if __name__ == "__main__":
    main()