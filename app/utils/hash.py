from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_key(plain_key: str, hashed_key: str) -> bool:
    """Verify if a given plain API key matches its hashed version."""
    return pwd_context.verify(plain_key, hashed_key)


def get_key_hash(key: str) -> str:
    """Hash a given API key using bcrypt and return its hashed version."""
    return pwd_context.hash(key)
