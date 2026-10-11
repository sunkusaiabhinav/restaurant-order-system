from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.menu_category import MenuCategory
from app.models.menu_item import MenuItem
from app.schemas.menu_item import (
    MenuItemCreate,
    MenuItemResponse,
)


router = APIRouter(
    prefix="/menu-items",
    tags=["Menu Items"]
)


@router.post(
    "/",
    response_model=MenuItemResponse,
    status_code=status.HTTP_201_CREATED
)
def create_menu_item(
    item_data: MenuItemCreate,
    db: Session = Depends(get_db)
):
    category = (
        db.query(MenuCategory)
        .filter(MenuCategory.id == item_data.category_id)
        .first()
    )

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu category not found"
        )

    menu_item = MenuItem(
        category_id=item_data.category_id,
        name=item_data.name,
        description=item_data.description,
        price=item_data.price,
        is_available=item_data.is_available
    )

    db.add(menu_item)
    db.commit()
    db.refresh(menu_item)

    return menu_item


@router.get(
    "/",
    response_model=list[MenuItemResponse]
)
def get_menu_items(
    db: Session = Depends(get_db)
):
    return (
        db.query(MenuItem)
        .order_by(MenuItem.id)
        .all()
    )


@router.get(
    "/{item_id}",
    response_model=MenuItemResponse
)
def get_menu_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    item = (
        db.query(MenuItem)
        .filter(MenuItem.id == item_id)
        .first()
    )

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found"
        )

    return item