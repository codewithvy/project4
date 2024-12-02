from database import SessionLocal, engine
from models import Base, Category, Product

Base.metadata.create_all(bind=engine)

def seed_data():
    db = SessionLocal()
    try:
        # Add categories
        electronics = Category(name="Electronics")
        home_appliances = Category(name="Home Appliances")
        db.add_all([electronics, home_appliances])
        db.commit()

        # Add products
        product1 = Product(
            name="Smartphone",
            description="A high-end smartphone",
            price=699.99,
            inventory=50,
            category_id=electronics.id
        )
        product2 = Product(
            name="Microwave",
            description="Compact microwave oven",
            price=89.99,
            inventory=100,
            category_id=home_appliances.id
        )
        db.add_all([product1, product2])
        db.commit()
        print("Data seeded successfully!")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()