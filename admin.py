import sqlite3

# Database setup: Connect to SQLite database (create it if it doesn't exist)
conn = sqlite3.connect("ecommerce.db")
cursor = conn.cursor()

# Create tables if they don't already exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        stock INTEGER NOT NULL
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        FOREIGN KEY (product_id) REFERENCES products (id)
    )
""")
conn.commit()

# Admin menu function
def admin_menu():
    while True:
        print("\nAdmin Menu:")
        print("1. View Products")
        print("2. Add Product")
        print("3. Update Product Stock")
        print("4. View Orders")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            view_products()
        elif choice == "2":
            add_product()
        elif choice == "3":
            update_product_stock()
        elif choice == "4":
            view_orders()
        elif choice == "5":
            print("Exiting admin panel. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

# Function to view all products
def view_products():
    print("\n[View Products]")
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    if products:
        for product in products:
            print(f"ID: {product[0]}, Name: {product[1]}, Price: ${product[2]:.2f}, Stock: {product[3]}")
    else:
        print("No products found.")

# Function to add a new product
def add_product():
    print("\n[Add Product]")
    name = input("Enter product name: ")
    price = input("Enter product price: ")
    stock = input("Enter product stock: ")

    try:
        price = float(price)
        stock = int(stock)
        cursor.execute("INSERT INTO products (name, price, stock) VALUES (?, ?, ?)", (name, price, stock))
        conn.commit()
        print(f"Product '{name}' added successfully!")
    except ValueError:
        print("Invalid price or stock. Please enter valid numbers.")

# Function to update product stock
def update_product_stock():
    print("\n[Update Product Stock]")
    product_id = input("Enter product ID: ")
    new_stock = input("Enter new stock quantity: ")

    try:
        product_id = int(product_id)
        new_stock = int(new_stock)
        cursor.execute("UPDATE products SET stock = ? WHERE id = ?", (new_stock, product_id))
        if cursor.rowcount > 0:
            conn.commit()
            print("Product stock updated successfully!")
        else:
            print("Product ID not found.")
    except ValueError:
        print("Invalid input. Please enter valid numbers.")

# Function to view all orders
def view_orders():
    print("\n[View Orders]")
    cursor.execute("""
        SELECT orders.id, products.name, orders.quantity 
        FROM orders 
        JOIN products ON orders.product_id = products.id
    """)
    orders = cursor.fetchall()
    if orders:
        for order in orders:
            print(f"Order ID: {order[0]}, Product: {order[1]}, Quantity: {order[2]}")
    else:
        print("No orders found.")

# Entry point
if __name__ == "__main__":
    admin_menu()

# Close the database connection when the program exits
conn.close()
