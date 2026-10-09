
from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column


from app.database.database import Base


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)

    customer_name: Mapped[str] = mapped_column(
        String(200)
    )

    customer_phone: Mapped[str] = mapped_column(
        String(50)
    )

    customer_address: Mapped[str] = mapped_column(
        String(500),
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="NEW"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )   