from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.order import Order
from app.schemas.order import OrderCreate, OrderResponse, OrderDetails
from app.models.order_item import OrderItem
from app.models.product import Product
from app.schemas.order_item import OrderItemDetails

router = APIRouter()


@router.post("/orders", response_model=OrderResponse)
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db)
):
    new_order = Order(
        customer_name=order.customer_name,
        customer_phone=order.customer_phone,
        customer_address=order.customer_address
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order

@router.get("/orders", response_model=list[OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    orders = db.query(Order).all()

    return orders

@router.get(
    "/orders/{order_id}/items",
    response_model=list[OrderItemDetails]
)
def get_order_items_by_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    items = (
        db.query(OrderItem, Product)
        .join(Product, OrderItem.product_id == Product.id)
        .filter(OrderItem.order_id == order_id)
        .all()
    )

    return [
        {
            "product_name": product.name,
            "quantity": order_item.quantity
        }
        for order_item, product in items
    ]


@router.get("/orders/{order_id}", response_model=OrderDetails)
def get_order_details(
    order_id: int,
    db: Session = Depends(get_db)
):
    order = db.get(Order, order_id)

    if order is None:
        return None

    items = (
        db.query(OrderItem, Product)
        .join(Product, OrderItem.product_id == Product.id)
        .filter(OrderItem.order_id == order_id)
        .all()
    )

    return {
        "id": order.id,
        "customer_name": order.customer_name,
        "customer_phone": order.customer_phone,
        "customer_address": order.customer_address,
        "status": order.status,
        "items": [
            {
                "product_name": product.name,
                "quantity": order_item.quantity
            }
            for order_item, product in items
        ]
    }