from pydantic import BaseModel
from typing import Optional
from enum import Enum

class Address(BaseModel):
    street: str
    city: str
    province: str
    postalcode: str

class UserRole(str, Enum):
    CUSTOMER = "customer"
    RESTAURANT = "restaurant"

class UserCreate(BaseModel):
    firstname: str
    lastname: str
    email: str
    password: str
    phone: Optional[str] = None
    address: Optional[Address] = None

class User(BaseModel):
    id: int
    role: UserRole
    firstname: str
    lastname: str
    email: str
    phone: Optional[str] = None
    address: Optional[Address] = None
    is_active: bool

