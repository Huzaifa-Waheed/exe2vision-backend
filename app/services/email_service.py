class EmailService:

    @staticmethod
    def send_otp_email(email: str, otp: str):
        print(f"[DEBUG] OTP for {email}: {otp}")
