from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.restaurant_table import RestaurantTable
from app.schemas.restaurant_table import (
    RestaurantTableCreate,
    RestaurantTableResponse,
)


router = APIRouter(
    prefix="/tables",
    tags=["Tables"]
)


@router.post(
    "/",
    response_model=RestaurantTableResponse,
    status_code=status.HTTP_201_CREATED
)
def create_table(
    table_data: RestaurantTableCreate,
    db: Session = Depends(get_db)
):
    existing_table = (
        db.query(RestaurantTable)
        .filter(
            RestaurantTable.table_number
            == table_data.table_number
        )
        .first()
    )

    if existing_table:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Table number already exists"
        )

    table = RestaurantTable(
        table_number=table_data.table_number,
        capacity=table_data.capacity
    )

    db.add(table)
    db.commit()
    db.refresh(table)

    return table


@router.get(
    "/",
    response_model=list[RestaurantTableResponse]
)
def get_tables(
    db: Session = Depends(get_db)
):
    return (
        db.query(RestaurantTable)
        .order_by(RestaurantTable.id)
        .all()
    )


@router.get(
    "/{table_id}",
    response_model=RestaurantTableResponse
)
def get_table(
    table_id: int,
    db: Session = Depends(get_db)
):
    table = (
        db.query(RestaurantTable)
        .filter(RestaurantTable.id == table_id)
        .first()
    )

    if not table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Table not found"
        )

    return table