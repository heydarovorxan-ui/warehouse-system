from sqlalchemy import String, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from app.database.database import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(200))

    description: Mapped[str] = mapped_column(String(1000))

    quantity: Mapped[int] = mapped_column(Integer)

    price: Mapped[float] = mapped_column(Float)

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id")
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )
    
    category = relationship("Category")

    @property
    def category_name(self):
        return self.category.name