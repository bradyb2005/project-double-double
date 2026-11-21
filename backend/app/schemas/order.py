from datetime import datetime

from pydantic import BaseModel, Field


class OrderItem(BaseModel):
    item_id: int
    name: str
    price: float = Field(..., gt=0, description = "Price must be greater than 0")
    quantity: int = Field(..., gt=0, description = "Quantity must be greater than 0")

class Order(BaseModel):
    id: int
    customer_id: int
    customer_details: dict
    restaurant_id: int
    items: list[OrderItem]
    subtotal: float = Field(..., ge=0, description="Sum of item prices × quantities")
    gst: float = Field(..., ge=0, description="GST (5% of subtotal)")
    pst: float = Field(..., ge=0, description="PST (7% of subtotal, BC only)")
    service_charge: float = Field(..., ge=0, description="Service charge (10% of subtotal)")
    total_price: float = Field(..., gt=0, description="Subtotal plus GST, PST and service charge")
    status: str = "pending"
    created_at: datetime
