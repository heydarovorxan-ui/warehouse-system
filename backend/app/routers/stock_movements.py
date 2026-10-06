from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.product import Product
from app.models.stock_movement import StockMovement
from app.models.user import User
from app.schemas.stock_movement import (
    StockMovementCreate,
    StockMovementResponse,
    StockMovementHistoryResponse
)
from app.security import require_roles

router = APIRouter()


@router.post(
    "/stock/receive",
    response_model=StockMovementResponse
)
def receive_stock(
    movement: StockMovementCreate,
    current_user = Depends(
        require_roles("admin", "warehouse")
    ),
    db: Session = Depends(get_db)
):
    product = db.get(Product, movement.product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    if movement.quantity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Quantity must be greater than 0"
        )

    product.quantity += movement.quantity

    new_movement = StockMovement(
        product_id=movement.product_id,
        quantity=movement.quantity,
        movement_type="RECEIPT",
        reason=movement.reason,
        user_id=current_user.id
    )

    db.add(new_movement)
    db.commit()
    db.refresh(new_movement)

    return new_movement


@router.post(
    "/stock/write-off",
    response_model=StockMovementResponse
)
def write_off_stock(
    movement: StockMovementCreate,
    current_user = Depends(
        require_roles("admin", "warehouse")
    ),
    db: Session = Depends(get_db)
):
    product = db.get(Product, movement.product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    if movement.quantity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Quantity must be greater than 0"
        )

    if product.quantity < movement.quantity:
        raise HTTPException(
            status_code=400,
            detail=f"Not enough stock for {product.name}"
        )

    product.quantity -= movement.quantity

    new_movement = StockMovement(
        product_id=movement.product_id,
        quantity=-movement.quantity,
        movement_type="WRITE_OFF",
        reason=movement.reason,
        user_id=current_user.id
    )

    db.add(new_movement)
    db.commit()
    db.refresh(new_movement)

    return new_movement


@router.get(
    "/stock/movements",
    response_model=list[StockMovementHistoryResponse]
)
def get_stock_movements(
    current_user = Depends(
        require_roles("admin", "warehouse", "expeditor")
    ),
    db: Session = Depends(get_db)
):
    movements = (
        db.query(
            StockMovement,
            Product.name.label("product_name"),
            User.username.label("username")
        )
        .join(
            Product,
            StockMovement.product_id == Product.id
        )
        .join(
            User,
            StockMovement.user_id == User.id
        )
        .order_by(
            StockMovement.id.desc()
        )
        .all()
    )

    result = []

    for movement, product_name, username in movements:
        result.append({
            "id": movement.id,
            "product_id": movement.product_id,
            "product_name": product_name,
            "quantity": movement.quantity,
            "movement_type": movement.movement_type,
            "reason": movement.reason,
            "user_id": movement.user_id,
            "username": username,
            "order_id": movement.order_id,
            "created_at": movement.created_at
        })

    return result