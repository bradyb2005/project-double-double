from pydantic import BaseModel, Field, field_validator


class CartItem(BaseModel):
    """Schema for an item in the shopping cart."""
    item_id: int = Field(..., description="ID of the menu item")
    restaurant_id: int = Field(..., description="ID of the restaurant")
    quantity: int = Field(..., gt=0, description="Quantity must be greater than 0")

    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, value: int) -> int:
        """Validates that the quantity is a positive integer."""
        if value <= 0:
            raise ValueError("Quantity must be greater than 0")
        return value

class Cart(BaseModel):
    """Schema for the shopping cart."""
    items: list[CartItem] = Field(default_factory=list, description="List of items in the cart")
    total: float = Field(default=0.0, description="Total price of the items in the cart")

    @field_validator("items")
    @classmethod
    def validate_items(cls, value: list[CartItem]) -> list[CartItem]:
        """Validate the cart items."""
        return value