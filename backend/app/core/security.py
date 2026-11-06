from passlib.context import CryptContext

# Set up the hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Takes a plain text password and returns a hashed string."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Checks if a plain text password matches the stored hashed version."""
    return pwd_context.verify(plain_password, hashed_password)