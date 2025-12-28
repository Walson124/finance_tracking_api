import bcrypt
import secrets
from datetime import datetime, timedelta, timezone

SESSION_TTL_DAYS = 30

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))

def new_session_token() -> str:
    return secrets.token_urlsafe(32)

def session_expiry():
    return datetime.now(timezone.utc) + timedelta(days=SESSION_TTL_DAYS)
