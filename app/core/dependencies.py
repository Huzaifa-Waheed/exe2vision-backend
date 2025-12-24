from fastapi import Depends, HTTPException, status, Request
from app.database.manager import DatabaseManager


def get_current_user(
    request: Request,
    db = Depends(DatabaseManager.get_db)
):
    """Authenticate user via a cookie named 'user_email'.

    This replaces the previous JWT-based approach so that client
    can rely on a simple session cookie set at login.
    """
    email = request.cookies.get("user_email")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    user = DatabaseManager.get_user_by_email(db, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user"
        )

    return user
