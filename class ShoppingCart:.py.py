class ShoppingCart:
    def __init__(self):
        self.items = {}

    def add_item(self, item_id, quantity, price):
        if item_id in self.items:
            self.items[item_id]['quantity'] += quantity
        else:
            self.items[item_id] = {'quantity': quantity, 'price': price}

    def remove_item(self, item_id):
        if item_id in self.items:
            del self.items[item_id]

    def update_quantity(self, item_id, quantity):
        if item_id in self.items:
            self.items[item_id]['quantity'] = quantity

    def get_total(self):
        total = 0
        for item in self.items.values():
            total += item['quantity'] * item['price']
        return total

    def get_items(self):
        return self.items

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