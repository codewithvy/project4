from flask import jsonify, request
from functools import wraps
from model import Product, Order, User, db

# =========================
# Role-Based Access Control
# =========================
def admin_only(func):
    """Decorator to ensure only admin users can access a function."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = request.headers.get('User-ID')  # Assume user ID is sent in request headers
        user = User.query.get(user_id)
        if not user or user.role != 'admin':
            return jsonify({"error": "Access denied. Admins only."}), 403
        return func(*args, **kwargs)
    return wrapper

# =========================
# Product Management
# =========================
@admin_only
def create_product(name, price, stock):
    """Create a new product."""
    try:
        product = Product(name=name, price=price, stock=stock)
        db.session.add(product)
        db.session.commit()
        return jsonify({"message": f"Product '{name}' created successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_products():
    """Get all products."""
    try:
        products = Product.query.all()
        return jsonify([{
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "stock": product.stock
        } for product in products]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_product_by_id(product_id):
    """Get a single product by ID."""
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({"error": "Product not found"}), 404
        return jsonify({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "stock": product.stock
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_only
def update_product(product_id, updates):
    """Update a product by its ID."""
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({"error": "Product not found"}), 404
        for key, value in updates.items():
            if hasattr(product, key):
                setattr(product, key, value)
        db.session.commit()
        return jsonify({"message": f"Product '{product_id}' updated successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_only
def delete_product(product_id):
    """Delete a product by its ID."""
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({"error": "Product not found"}), 404
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": f"Product '{product_id}' deleted successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# =========================
# Order Management
# =========================
@admin_only
def create_order(product_id, quantity, total_price):
    """Create a new order."""
    try:
        order = Order(product_id=product_id, quantity=quantity, total_price=total_price)
        db.session.add(order)
        db.session.commit()
        return jsonify({"message": "Order created successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_orders():
    """Get all orders."""
    try:
        orders = Order.query.all()
        return jsonify([{
            "id": order.id,
            "product_id": order.product_id,
            "quantity": order.quantity,
            "total_price": order.total_price,
            "status": order.status
        } for order in orders]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_order_by_id(order_id):
    """Get a single order by ID."""
    try:
        order = Order.query.get(order_id)
        if not order:
            return jsonify({"error": "Order not found"}), 404
        return jsonify({
            "id": order.id,
            "product_id": order.product_id,
            "quantity": order.quantity,
            "total_price": order.total_price,
            "status": order.status
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_only
def update_order(order_id, updates):
    """Update an order by its ID."""
    try:
        order = Order.query.get(order_id)
        if not order:
            return jsonify({"error": "Order not found"}), 404
        for key, value in updates.items():
            if hasattr(order, key):
                setattr(order, key, value)
        db.session.commit()
        return jsonify({"message": f"Order '{order_id}' updated successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_only
def delete_order(order_id):
    """Delete an order by its ID."""
    try:
        order = Order.query.get(order_id)
        if not order:
            return jsonify({"error": "Order not found"}), 404
        db.session.delete(order)
        db.session.commit()
        return jsonify({"message": f"Order '{order_id}' deleted successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# =========================
# Analytics
# =========================
def get_sales_metrics():
    """Get total sales and top-selling products."""
    try:
        total_sales = db.session.query(db.func.sum(Order.total_price)).scalar()
        top_products = db.session.query(
            Product.name, db.func.count(Order.id)
        ).join(Order, Product.id == Order.product_id)\
         .group_by(Product.name)\
         .order_by(db.func.count(Order.id).desc())\
         .limit(5)\
         .all()
        top_products_list = [{"product": name, "orders": count} for name, count in top_products]
        return jsonify({
            "total_sales": total_sales,
            "top_products": top_products_list
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_active_users():
    """Get a count of active users."""
    try:
        active_users_count = User.query.filter_by(active=True).count()
        return jsonify({"active_users": active_users_count}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
