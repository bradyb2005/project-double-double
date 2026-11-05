from pydantic import BaseModel, EmailStr
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

class UserRole(str, Enum):
    CUSTOMER = "customer"
    RESTAURANT = "restaurant"

class UserCreate(BaseModel):
    role: UserRole = UserRole.CUSTOMER
    firstname: str
    lastname: str
    email: EmailStr
    password: str
    phone: Optional[str] = None
    address: Optional[Address] = None
    is_active: bool = True

class User(BaseModel):
    id: int
    role: UserRole
    firstname: str
    lastname: str
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[Address] = None
    is_active: bool

