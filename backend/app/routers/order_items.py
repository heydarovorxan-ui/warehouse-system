from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.order_item import OrderItem
from app.schemas.order_item import (
    OrderItemCreate,
    OrderItemResponse
)

router = APIRouter()


@router.post("/order-items", response_model=OrderItemResponse)
def create_order_item(
    order_item: OrderItemCreate,
    db: Session = Depends(get_db)
):
    new_order_item = OrderItem(
        order_id=order_item.order_id,
        product_id=order_item.product_id,
        quantity=order_item.quantity
    )

    db.add(new_order_item)
    db.commit()
    db.refresh(new_order_item)

    return new_order_item

@router.get("/order-items", response_model=list[OrderItemResponse])
def get_order_items(db: Session = Depends(get_db)):
    order_items = db.query(OrderItem).all()

    return order_items