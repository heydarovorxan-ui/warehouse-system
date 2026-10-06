from datetime import datetime

from sqlalchemy import String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


class StockMovement(Base):
    __tablename__ = "stock_movements"

    id: Mapped[int] = mapped_column(primary_key=True)

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id")
    )

    quantity: Mapped[int] = mapped_column(Integer)

    movement_type: Mapped[str] = mapped_column(
        String(50)
    )

    reason: Mapped[str] = mapped_column(
        String(500),
        nullable=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id"),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )