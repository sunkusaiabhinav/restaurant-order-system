from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.customer import Customer
from app.models.menu_item import MenuItem
from app.models.order import Order, OrderStatus
from app.models.order_item import OrderItem
from app.models.restaurant_table import (
    RestaurantTable,
    TableStatus,
)
from app.schemas.order import OrderCreate, OrderResponse


router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

from app.schemas.order import (
    OrderCreate,
    OrderResponse,
    OrderStatusUpdate,
)


@router.post(
    "/",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED
)
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db)
):
    # --------------------------------------------------
    # 1. Lock the table row
    # --------------------------------------------------

    table = (
        db.query(RestaurantTable)
        .filter(RestaurantTable.id == order_data.table_id)
        .with_for_update()
        .first()
    )

    if not table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant table not found"
        )

    # --------------------------------------------------
    # 2. Check table availability
    # --------------------------------------------------

    if table.status != TableStatus.AVAILABLE:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Restaurant table is already occupied"
        )

    # --------------------------------------------------
    # 3. Check customer
    # --------------------------------------------------

    customer = (
        db.query(Customer)
        .filter(Customer.id == order_data.customer_id)
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )

    # --------------------------------------------------
    # 4. Prevent duplicate menu items
    # --------------------------------------------------

    menu_item_ids = [
        item.menu_item_id
        for item in order_data.items
    ]

    if len(menu_item_ids) != len(set(menu_item_ids)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Duplicate menu items are not allowed in one order"
        )

    # --------------------------------------------------
    # 5. Fetch menu items
    # --------------------------------------------------

    menu_items = (
        db.query(MenuItem)
        .filter(MenuItem.id.in_(menu_item_ids))
        .all()
    )

    menu_items_by_id = {
        item.id: item
        for item in menu_items
    }

    # --------------------------------------------------
    # 6. Validate menu items
    # --------------------------------------------------

    for item_data in order_data.items:

        menu_item = menu_items_by_id.get(
            item_data.menu_item_id
        )

        if not menu_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(
                    f"Menu item "
                    f"{item_data.menu_item_id} not found"
                )
            )

        if not menu_item.is_available:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    f"Menu item '{menu_item.name}' "
                    f"is currently unavailable"
                )
            )

    # --------------------------------------------------
    # 7. Create order
    # --------------------------------------------------

    order = Order(
        customer_id=order_data.customer_id,
        table_id=order_data.table_id,
        status=OrderStatus.PLACED,
        total_amount=Decimal("0.00")
    )

    db.add(order)

    # Flush so order.id is generated before creating items
    db.flush()

    # --------------------------------------------------
    # 8. Create order items
    # --------------------------------------------------

    total_amount = Decimal("0.00")

    for item_data in order_data.items:

        menu_item = menu_items_by_id[
            item_data.menu_item_id
        ]

        unit_price = menu_item.price

        subtotal = (
            unit_price * item_data.quantity
        )

        order_item = OrderItem(
            order_id=order.id,
            menu_item_id=menu_item.id,
            quantity=item_data.quantity,
            unit_price=unit_price,
            subtotal=subtotal
        )

        db.add(order_item)

        total_amount += subtotal

    # --------------------------------------------------
    # 9. Update order total
    # --------------------------------------------------

    order.total_amount = total_amount

    # --------------------------------------------------
    # 10. Occupy the table
    # --------------------------------------------------

    table.status = TableStatus.OCCUPIED

    # --------------------------------------------------
    # 11. Commit everything atomically
    # --------------------------------------------------

    db.commit()

    db.refresh(order)

    return order

@router.patch(
    "/{order_id}/status",
    response_model=OrderResponse
)
def update_order_status(
    order_id: int,
    status_data: OrderStatusUpdate,
    db: Session = Depends(get_db)
):
    order = (
        db.query(Order)
        .filter(Order.id == order_id)
        .with_for_update()
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    current_status = order.status
    new_status = status_data.status

    allowed_transitions = {
        OrderStatus.PLACED: {
            OrderStatus.CONFIRMED,
            OrderStatus.CANCELLED,
        },
        OrderStatus.CONFIRMED: {
            OrderStatus.PREPARING,
            OrderStatus.CANCELLED,
        },
        OrderStatus.PREPARING: {
            OrderStatus.READY,
        },
        OrderStatus.READY: {
            OrderStatus.COMPLETED,
        },
        OrderStatus.COMPLETED: set(),
        OrderStatus.CANCELLED: set(),
    }

    if new_status not in allowed_transitions[current_status]:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                f"Invalid status transition: "
                f"{current_status.value} -> {new_status.value}"
            )
        )

    order.status = new_status

    db.commit()
    db.refresh(order)

    return order

@router.get(
    "/{order_id}",
    response_model=OrderResponse
)
def get_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    order = (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    return order