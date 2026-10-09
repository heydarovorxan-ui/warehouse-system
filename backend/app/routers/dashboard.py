from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.database import get_db
from app.models.product import Product
from app.models.category import Category
from app.models.order import Order
from app.models.stock_movement import StockMovement
from app.security import require_roles

router = APIRouter()


@router.get("/dashboard")
def get_dashboard(
    current_user = Depends(
        require_roles("admin", "warehouse", "expeditor")
    ),
    db: Session = Depends(get_db)
):
    now = datetime.utcnow()

    month_start = datetime(
        now.year,
        now.month,
        1
    )

    total_products = db.query(
        func.count(Product.id)
    ).scalar()

    total_categories = db.query(
        func.count(Category.id)
    ).scalar()

    total_orders = db.query(
        func.count(Order.id)
    ).scalar()

    new_orders = db.query(
        func.count(Order.id)
    ).filter(
        Order.status == "NEW"
    ).scalar()

    confirmed_orders = db.query(
        func.count(Order.id)
    ).filter(
        Order.status == "CONFIRMED"
    ).scalar()

    orders_this_month = db.query(
        func.count(Order.id)
    ).filter(
        Order.created_at >= month_start
    ).scalar()

    products_this_month = db.query(
        func.count(Product.id)
    ).filter(
        Product.created_at >= month_start
    ).scalar()

    stock_value = db.query(
        func.coalesce(
            func.sum(Product.quantity * Product.price),
            0
        )
    ).scalar()

    received_this_month = db.query(
        func.coalesce(
            func.sum(StockMovement.quantity),
            0
        )
    ).filter(
        StockMovement.movement_type == "RECEIPT",
        StockMovement.created_at >= month_start
    ).scalar()

    written_off_this_month = db.query(
        func.coalesce(
            func.sum(-StockMovement.quantity),
            0
        )
    ).filter(
        StockMovement.movement_type == "WRITE_OFF",
        StockMovement.created_at >= month_start
    ).scalar()

    return {
        "total_products": total_products,
        "total_categories": total_categories,
        "total_orders": total_orders,
        "new_orders": new_orders,
        "confirmed_orders": confirmed_orders,
        "orders_this_month": orders_this_month,
        "products_this_month": products_this_month,
        "stock_value": stock_value,
        "received_this_month": received_this_month,
        "written_off_this_month": written_off_this_month
    }