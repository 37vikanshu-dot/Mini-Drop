import logging
import bcrypt
import secrets


def hash_password(password: str) -> str:
    try:
        password_bytes = password.encode("utf-8")
        if len(password_bytes) > 72:
            password_bytes = password_bytes[:72]
        hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        return hashed.decode("utf-8")
    except Exception as e:
        logging.exception(f"Error hashing password: {e}")
        return ""


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        if not hashed_password:
            return False
        password_bytes = plain_password.encode("utf-8")
        if len(password_bytes) > 72:
            password_bytes = password_bytes[:72]
        hashed_bytes = hashed_password.encode("utf-8")
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception as e:
        logging.exception(f"Error verifying password: {e}")
        return False


def generate_session_token() -> str:
    return secrets.token_urlsafe(32)