from pydantic import BaseModel


class OrderItemCreate(BaseModel):
    order_id: int
    product_id: int
    quantity: int


class OrderItemResponse(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int

    class Config:
        from_attributes = True


class OrderItemDetails(BaseModel):
    product_name: str
    quantity: int