from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Product, Order, User
import sys

# Initialize the database
from models import Base
Base.metadata.create_all(bind=engine)

def fetch_products(db: Session):
    """Display all available products."""
    products = db.query(Product).all()
    if not products:
        print("\nNo products available.")
        return []
    
    print("\nAvailable Products:")
    print("-------------------")
    for product in products:
        print(f"ID: {product.id}, Name: {product.name}, Price: ${product.price:.2f}, Stock: {product.stock}")
    print("-------------------")
    return products

def fetch_orders(db: Session, user=None, is_admin=False):
    """Fetch and display orders."""
    if is_admin:
        orders = db.query(Order).all()
    else:
        orders = db.query(Order).filter_by(user_id=user.id).all()

    if not orders:
        print("\nNo orders found.")
        return []

    print("\nYour Orders:" if not is_admin else "\nAll Orders:")
    print("-------------------")
    for order in orders:
        print(
            f"Order ID: {order.id}, Product ID: {order.product_id}, Quantity: {order.quantity}, "
            f"Total: ${order.total_price:.2f}, Status: {order.status}"
        )
    print("-------------------")
    return orders

def create_order(db: Session, user):
    """Allow a user to create an order."""
    fetch_products(db)
    try:
        product_id = int(input("Enter Product ID to purchase: "))
        quantity = int(input("Enter quantity: "))
    except ValueError:
        print("Invalid input. Please try again.")
        return

    product = db.query(Product).filter_by(id=product_id).first()
    if not product:
        print("Product not found.")
        return

    if product.stock < quantity:
        print(f"Insufficient stock. Only {product.stock} available.")
        return

    # Update product stock
    product.stock -= quantity
    total_price = product.price * quantity

    # Create the order
    order = Order(user_id=user.id, product_id=product.id, quantity=quantity, total_price=total_price, status="Pending")
    db.add(order)
    db.commit()
    print(f"\nOrder created successfully! Total Price: ${total_price:.2f}")

def update_order_status(db: Session):
    """Admin functionality to update order status."""
    fetch_orders(db, is_admin=True)
    try:
        order_id = int(input("Enter Order ID to update: "))
        new_status = input("Enter new status (Pending/Shipped/Delivered): ").capitalize()
        if new_status not in ["Pending", "Shipped", "Delivered"]:
            print("Invalid status. Please try again.")
            return
    except ValueError:
        print("Invalid input. Please try again.")
        return

    order = db.query(Order).filter_by(id=order_id).first()
    if not order:
        print("Order not found.")
        return

    order.status = new_status
    db.commit()
    print(f"\nOrder ID {order_id} status updated to '{new_status}'.")

# =========================
# User Authentication
# =========================

def login_user(db: Session):
    """Login a user."""
    username = input("Enter your username: ").strip()
    user = db.query(User).filter_by(username=username).first()

    if not user:
        print("User not found. Please register.")
        return None

    print(f"Welcome, {username}!")
    return user

def admin_check(user):
    """Check if the user is an admin."""
    return user.role == "admin"

# =========================
# Main Terminal UI
# =========================

def main():
    db = SessionLocal()
    current_user = None

    try:
        while not current_user:
            print("\n=== Welcome to the E-Commerce Store ===")
            print("1. Login")
            print("2. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                current_user = login_user(db)
            elif choice == "2":
                print("Goodbye!")
                sys.exit()
            else:
                print("Invalid choice. Please try again.")

        while True:
            if admin_check(current_user):
                print("\n=== Admin Menu ===")
                print("1. View All Orders")
                print("2. Update Order Status")
                print("3. View Products")
                print("4. Logout")
                print("5. Exit")
                choice = input("Enter your choice: ")

                if choice == "1":
                    fetch_orders(db, is_admin=True)
                elif choice == "2":
                    update_order_status(db)
                elif choice == "3":
                    fetch_products(db)
                elif choice == "4":
                    current_user = None
                    break
                elif choice == "5":
                    print("Goodbye!")
                    sys.exit()
                else:
                    print("Invalid choice. Please try again.")
            else:
                print("\n=== User Menu ===")
                print("1. View Your Orders")
                print("2. Create Order")
                print("3. View Products")
                print("4. Logout")
                print("5. Exit")
                choice = input("Enter your choice: ")

                if choice == "1":
                    fetch_orders(db, user=current_user)
                elif choice == "2":
                    create_order(db, current_user)
                elif choice == "3":
                    fetch_products(db)
                elif choice == "4":
                    current_user = None
                    break
                elif choice == "5":
                    print("Goodbye!")
                    sys.exit()
                else:
                    print("Invalid choice. Please try again.")
    finally:
        db.close()

if __name__ == "__main__":
    main()