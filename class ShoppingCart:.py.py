from sqlalchemy.orm import Session
from models import CartItem, Product

class ShoppingCart:
    def __init__(self, db: Session):
        self.db = db

    def add_item(self, product_id, quantity):
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if not product or product.inventory < quantity:
            raise ValueError("Product not available or insufficient inventory")

        cart_item = self.db.query(CartItem).filter(CartItem.product_id == product_id).first()
        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = CartItem(product_id=product_id, quantity=quantity, price=product.price)
            self.db.add(cart_item)

        self.db.commit()

    def remove_item(self, product_id):
        cart_item = self.db.query(CartItem).filter(CartItem.product_id == product_id).first()
        if cart_item:
            self.db.delete(cart_item)
            self.db.commit()

    def update_quantity(self, product_id, quantity):
        cart_item = self.db.query(CartItem).filter(CartItem.product_id == product_id).first()
        if not cart_item:
            raise ValueError("Item not in cart")
        cart_item.quantity = quantity
        self.db.commit()

    def get_total(self):
        total = (
            self.db.query(CartItem)
            .with_entities(
                (CartItem.quantity * CartItem.price).label("total")
            )
            .all()
        )
        return sum(item.total for item in total)

    def get_items(self):
        cart_items = self.db.query(CartItem).all()
        return [{"product_id": item.product_id, "quantity": item.quantity, "price": item.price} for item in cart_items]


class Checkout : 
    def __init__(self, cart):
        self.cart = cart
        self.payment_method = None
        self.shipping_address = None

    def set_payment_method(self, payment_method):
        self.payment_method = payment_method

    def set_shipping_address(self, shipping_address):
        self.shipping_address = shipping_address

    def process_payment(self):
        total = self.cart.get_total()
        if self.payment_method == 'credit_card':
            print(f'Charging {total} to credit card')
        elif self.payment_method == 'paypal':
            print(f'Charging {total} to PayPal')
        else:
            print('No payment method set')

    def process_shipping(self):
        if self.shipping_address:
            print(f'Shipping items to {self.shipping_address}')
        else:
            print('No shipping address set')
