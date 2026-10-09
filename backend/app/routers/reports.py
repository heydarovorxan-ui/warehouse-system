from datetime import datetime
from io import BytesIO

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from openpyxl import Workbook

from app.database.database import get_db
from app.models.order import Order
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