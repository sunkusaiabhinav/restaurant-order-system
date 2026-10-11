from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.menu_category import MenuCategory
from app.schemas.menu_category import (
    MenuCategoryCreate,
    MenuCategoryResponse,
)


router = APIRouter(
    prefix="/menu-categories",
    tags=["Menu Categories"]
)


@router.post(
    "/",
    response_model=MenuCategoryResponse,
    status_code=status.HTTP_201_CREATED
)
def create_category(
    category_data: MenuCategoryCreate,
    db: Session = Depends(get_db)
):
    existing_category = (
        db.query(MenuCategory)
        .filter(MenuCategory.name == category_data.name)
        .first()
    )

    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Menu category already exists"
        )

    category = MenuCategory(
        name=category_data.name,
        description=category_data.description
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    return category


@router.get(
    "/",
    response_model=list[MenuCategoryResponse]
)
def get_categories(
    db: Session = Depends(get_db)
):
    return (
        db.query(MenuCategory)
        .order_by(MenuCategory.id)
        .all()
    )