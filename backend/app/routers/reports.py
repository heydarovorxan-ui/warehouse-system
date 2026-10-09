from datetime import datetime
from io import BytesIO

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from openpyxl import Workbook

from app.database.database import get_db
from app.models.order import Order
from app.models.stock_movement import StockMovement
from app.models.product import Product
from app.models.user import User
from app.security import require_roles


router = APIRouter()


@router.get("/reports/orders")
def get_orders_report(
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    status: str | None = None,
    current_user=Depends(
        require_roles("admin", "warehouse", "expeditor")
    ),
    db: Session = Depends(get_db)
):
    query = db.query(Order)

    if date_from:
        query = query.filter(Order.created_at >= date_from)

    if date_to:
        query = query.filter(Order.created_at <= date_to)

    if status:
        query = query.filter(Order.status == status)

    orders = query.order_by(Order.created_at.desc()).all()

    return orders


@router.get("/reports/orders/excel")
def export_orders_report_excel(
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    status: str | None = None,
    current_user=Depends(
        require_roles("admin", "warehouse", "expeditor")
    ),
    db: Session = Depends(get_db)
):
    query = db.query(Order)

    if date_from:
        query = query.filter(Order.created_at >= date_from)

    if date_to:
        query = query.filter(Order.created_at <= date_to)

    if status:
        query = query.filter(Order.status == status)

    orders = query.order_by(Order.created_at.desc()).all()

    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Orders Report"

    worksheet.append([
        "ID",
        "Customer",
        "Phone",
        "Address",
        "Status",
        "Created"
    ])

    for order in orders:
        worksheet.append([
            order.id,
            order.customer_name,
            order.customer_phone,
            order.customer_address or "",
            order.status,
            order.created_at
        ])

    output = BytesIO()

    workbook.save(output)

    output.seek(0)

    return StreamingResponse(
        output,
        media_type=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        ),
        headers={
            "Content-Disposition":
                "attachment; filename=orders_report.xlsx"
        }
    )


@router.get("/reports/stock-movements")
def get_stock_movements_report(
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    movement_type: str | None = None,
    current_user=Depends(
        require_roles("admin", "warehouse", "expeditor")
    ),
    db: Session = Depends(get_db)
):
    query = (
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
    )

    if date_from:
        query = query.filter(
            StockMovement.created_at >= date_from
        )

    if date_to:
        query = query.filter(
            StockMovement.created_at <= date_to
        )

    if movement_type:
        query = query.filter(
            StockMovement.movement_type == movement_type
        )

    movements = query.order_by(
        StockMovement.created_at.desc()
    ).all()

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


@router.get("/reports/stock-movements/excel")
def export_stock_movements_report_excel(
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    movement_type: str | None = None,
    current_user=Depends(
        require_roles("admin", "warehouse", "expeditor")
    ),
    db: Session = Depends(get_db)
):
    query = (
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
    )

    if date_from:
        query = query.filter(
            StockMovement.created_at >= date_from
        )

    if date_to:
        query = query.filter(
            StockMovement.created_at <= date_to
        )

    if movement_type:
        query = query.filter(
            StockMovement.movement_type == movement_type
        )

    movements = query.order_by(
        StockMovement.created_at.desc()
    ).all()

    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Stock Movements"

    worksheet.append([
        "ID",
        "Product",
        "Movement Type",
        "Quantity",
        "Reason",
        "User",
        "Order ID",
        "Created"
    ])

    for movement, product_name, username in movements:
        worksheet.append([
            movement.id,
            product_name,
            movement.movement_type,
            movement.quantity,
            movement.reason or "",
            username,
            movement.order_id or "",
            movement.created_at
        ])

    output = BytesIO()
    workbook.save(output)
    output.seek(0)

    return StreamingResponse(
        output,
        media_type=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        ),
        headers={
            "Content-Disposition":
                "attachment; filename=stock_movements_report.xlsx"
        }
    )