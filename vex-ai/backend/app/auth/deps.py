from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.auth.jwt import decode_token

security = HTTPBearer()


class User:
    def __init__(self, username: str, role: str):
        self.username = username
        self.role = role


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    token = credentials.credentials
    try:
        payload = decode_token(token)
        return User(payload.get("sub", "anon"), payload.get("role", "VIEWER"))
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


def require_role(role: str):
    def wrapper(user: User = Depends(get_current_user)) -> User:
        roles_order = ["VIEWER", "TRADER", "ADMIN"]
        if roles_order.index(user.role) < roles_order.index(role):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient role")
        return user

    return wrapper
