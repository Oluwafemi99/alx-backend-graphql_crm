# seed_db.py

from crm.models import Customer, Product, Order
from django.utils import timezone


def run():

    Customer.objects.all().delete()

    # Create a single customer
    alice = Customer.objects.create(
        name="Alice",
        email="alice@example.com",
        phone="+1234567890"
    )

    # Bulk create customers
    bob = Customer.objects.create(
        name="Bob",
        email="bob@example.com",
        phone="123-456-7890"
    )
    carol = Customer.objects.create(
        name="Carol",
        email="carol@example.com"
        # phone is optional
    )

    # Create products
    laptop = Product.objects.create(
        name="Laptop",
        price=999.99,
        stock=10
    )
    mouse = Product.objects.create(
        name="Mouse",
        price=49.99,
        stock=50
    )

    # Create an order for Alice with Laptop and Mouse
    order = Order.objects.create(
        customer=alice,
        order_date=timezone.now()
    )
    order.products.set([laptop, mouse])
    order.total_amount = laptop.price + mouse.price
    order.save()

    print("✅ Database seeded successfully.")
