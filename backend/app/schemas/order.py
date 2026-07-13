from pydantic import BaseModel


class OrderCreate(BaseModel):
    customer_name: str
    customer_phone: str
    customer_address: str | None = None


class OrderResponse(BaseModel):
    id: int
    customer_name: str
    customer_phone: str
    customer_address: str | None = None
    status: str

    class Config:
        from_attributes = True

class OrderDetails(BaseModel):
    id: int
    customer_name: str
    customer_phone: str
    customer_address: str | None = None
    status: str
    items: list

    class Config:
        from_attributes = True