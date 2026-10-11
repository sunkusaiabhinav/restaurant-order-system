from decimal import Decimal

from app.schemas.customer import CustomerCreate
from app.schemas.restaurant_table import RestaurantTableCreate
from app.schemas.menu_category import MenuCategoryCreate
from app.schemas.menu_item import MenuItemCreate
from app.schemas.order import OrderCreate
from app.schemas.payment import PaymentCreate


customer = CustomerCreate(
    name="Abhi",
    phone="9876543210",
    email="abhi@example.com",
)

print("Customer:")
print(customer)


table = RestaurantTableCreate(
    table_number="T1",
    capacity=4,
)

print("\nTable:")
print(table)


category = MenuCategoryCreate(
    name="Main Course",
    description="Main course dishes",
)

print("\nCategory:")
print(category)


menu_item = MenuItemCreate(
    category_id=1,
    name="Chicken Biryani",
    description="Hyderabadi chicken biryani",
    price=Decimal("250.00"),
)

print("\nMenu Item:")
print(menu_item)


order = OrderCreate(
    customer_id=1,
    table_id=1,
    items=[
        {
            "menu_item_id": 1,
            "quantity": 2,
        }
    ],
)

print("\nOrder:")
print(order)


payment = PaymentCreate(
    order_id=1,
    amount=Decimal("500.00"),
)

print("\nPayment:")
print(payment)