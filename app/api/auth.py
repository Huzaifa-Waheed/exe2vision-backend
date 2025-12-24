from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from app.schemas.auth import RegisterSchema, LoginSchema, ResetPasswordSchema
from app.services.account_manager import AccountManager
from app.database.manager import DatabaseManager

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register")
def register(
    data: RegisterSchema,
    response: Response,
    db: Session = Depends(DatabaseManager.get_db)
):
    user = AccountManager.register_user(db, data)
    # Auto-login the user by setting a session cookie
    response.set_cookie(key="user_email", value=user.email, httponly=True, samesite="lax")
    return {
        "message": "User registered successfully",
        "user": user.to_dict()
    }

@router.post("/login")
def login(
    data: LoginSchema,
    response: Response,
    db: Session = Depends(DatabaseManager.get_db)
):
    user = AccountManager.login_user(db, data.email, data.password)
    # Set a simple session cookie to indicate authentication on subsequent requests
    response.set_cookie(key="user_email", value=user.email, httponly=True, samesite="lax")
    return {
        "message": "Login successful",
        "user": user.to_dict()
    }

@router.post("/logout")
def logout(
    response: Response
):
    response.delete_cookie("user_email")
    return {"message": "Logged out"}

@router.post("/request-reset")
def request_password_reset(
    data: dict,
    db: Session = Depends(DatabaseManager.get_db)
):
    # expected body: {"email": "user@example.com"}
    email = data.get("email")
    if not email:
        return {"message": "Email is required"}
    AccountManager.send_otp(db, email)
    return {"message": "OTP sent if email exists"}

@router.post("/reset-password")
def reset_password(
    data: ResetPasswordSchema,
    db: Session = Depends(DatabaseManager.get_db)
):
    # data should include: email, otp_code, new_password
    # we forward to AccountManager
    AccountManager.reset_password(db, data.email, data.otp_code, data.new_password)
    return {"message": "Password has been reset. Please login."} 
