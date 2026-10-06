from datetime import datetime

from pydantic import BaseModel


class StockMovementCreate(BaseModel):
    product_id: int
    quantity: int
    reason: str | None = None


class StockMovementResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    movement_type: str
    reason: str | None
    user_id: int
    order_id: int | None
    created_at: datetime

    class Config:
        from_attributes = True


class StockMovementHistoryResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    quantity: int
    movement_type: str
    reason: str | None
    user_id: int
    username: str
    order_id: int | None
    created_at: datetime

    class Config:
        from_attributes = True