from fastapi import FastAPI

from app.routers import customers
from app.routers import tables
from app.routers import menu_categories
from app.routers import menu_items
from app.routers import orders
from app.routers import payments


app = FastAPI(
    title="Restaurant Order Management System",
    version="1.0.0"
)


app.include_router(customers.router)
app.include_router(tables.router)
app.include_router(menu_categories.router)
app.include_router(menu_items.router)
app.include_router(orders.router)
app.include_router(payments.router)


@app.get("/")
def root():
    return {
        "message": "Restaurant Order Management API"
    }