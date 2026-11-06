from datetime import datetime
from enum import Enum

from pydantic import BaseModel, EmailStr, Field, field_validator


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
    phone: str | None = Field(default=None, pattern=r"^\d{10}$")
    address: Address | None = None
    is_active: bool = True

    @field_validator('phone')
    @classmethod
    def clean_phone(cls, value: str | None) -> str | None:
        """Cleans the phone number by removing non-digit characters."""
        if value is None:
            return value
        return "".join(char for char in value if char.isdigit())

class UserCreate(UserBase):
    """Schema for creating a new user, including the `password` field."""
    password: str = Field(..., min_length=8, max_length=128)

class UserUpdate(UserBase):
    """Schema for updating user information. All fields are optional."""
    firstname: str | None = None
    lastname: str | None = None
    email: EmailStr | None = None
    phone: str | None = Field(default=None, pattern=r"^\d{10}$")
    address: Address | None = None
    is_active: bool | None = None

class User(UserBase):
    """Schema for what is saved to users.json."""
    id: int
    created_at: datetime
    last_updated: datetime