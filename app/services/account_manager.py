# from app.database.manager import DatabaseManager
# from app.services.email_service import EmailService
# from app.core.security import hash_password, create_access_token
# from app.utils.otp import generate_otp
# from datetime import timedelta

# class AccountManager:

#     def register_user(self, data):
#         if DatabaseManager.get_user_by_email(data.email):
#             raise Exception("Email already exists")

#         user = DatabaseManager.create_user(
#             name=data.name,
#             email=data.email,
#             password_hash=hash_password(data.password)
#         )
#         return user

#     def login_user(self, email, pwd):
#         user = DatabaseManager.get_user_by_email(email)
#         if not user or not user.verify_password(pwd):
#             raise Exception("Invalid credentials")
#         return create_access_token({"sub": user.email, "role": user.role})

#     def send_otp(self, email):
#         otp = generate_otp()
#         DatabaseManager.save_otp(email, otp)
#         EmailService.send_otp_email(email, otp)

#     def reset_password(self, email, new_pwd):
#         DatabaseManager.update_password(email, hash_password(new_pwd))


from fastapi import HTTPException, status
from app.database.manager import DatabaseManager
from app.core.security import hash_password

class AccountManager:

    @staticmethod
    def register_user(db, data):
        existing_user = DatabaseManager.get_user_by_email(db, data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        user = DatabaseManager.create_user(
            db=db,
            name=data.name,
            email=data.email,
            password_hash=hash_password(data.password)
        )
        return user

    @staticmethod
    def login_user(db, email: str, password: str):
        user = DatabaseManager.get_user_by_email(db, email)

        if not user or not user.verify_password(password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        # Return the user object; session will be established via cookie in the API layer
        return user

    @staticmethod
    def send_otp(db, email: str):
        user = DatabaseManager.get_user_by_email(db, email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email not registered")
        from app.utils.otp import generate_otp
        from app.services.email_service import EmailService

        otp = generate_otp()
        DatabaseManager.save_otp(db, email, otp)
        EmailService.send_otp_email(email, otp)
        return True

    @staticmethod
    def reset_password(db, email: str, otp_code: str, new_password: str):
        # verify otp
        ok = DatabaseManager.verify_and_consume_otp(db, email, otp_code)
        if not ok:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired OTP")

        DatabaseManager.update_password(db, email, hash_password(new_password))
        return True
