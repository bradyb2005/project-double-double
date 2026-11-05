from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from enum import Enum

class Province(str, Enum):
    ON = "ON"
    QC = "QC"
    NS = "NS"
    NB = "NB"
    MB = "MB"
    BC = "BC"
    PE = "PE"
    SK = "SK"
    AB = "AB"
    NL = "NL"
class Address(BaseModel):
    street: str
    city: str
    province: Province
    postalcode: str

    @field_validator("postalcode")
    @classmethod
    def clean_postalcode(cls, value: str) -> str:
        """Cleans the postal code by removing spaces and converting to uppercase."""
        return value.replace(" ", "").upper()
class UserRole(str, Enum):
    """Enumeration of user roles."""
    CUSTOMER = "customer"
    RESTAURANT = "restaurant"

class UserBase(BaseModel):
    """Shared fields across all User schemas.
    The defaults are:
    - role: UserRole.CUSTOMER
    - is_active: True"""
    role: UserRole = UserRole.CUSTOMER
    firstname: str
    lastname: str
    email: EmailStr
    phone: Optional[str] = Field(default=None, pattern=r"^\d{10}$")
    address: Optional[Address] = None
    is_active: bool = True

    @field_validator('phone')
    @classmethod
    def clean_phone(cls, value: Optional[str]) -> Optional[str]:
        """Cleans the phone number by removing non-digit characters."""
        if value is None:
            return value
        return "".join(char for char in value if char.isdigit())

class UserCreate(UserBase):
    """Schema for creating a new user, including the `password` field."""
    password: str = Field(..., min_length=8, max_length=128)

class User(UserBase):
    """Schema for returning user data, excluding sensitive information."""
    id: int
    created_at: datetime
    updated_at: datetime