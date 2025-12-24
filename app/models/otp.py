from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timedelta
from app.database.base import Base

class OTPRecord(Base):
    __tablename__ = "otp_records"

    id = Column(Integer, primary_key=True)
    email = Column(String, index=True)
    otp_code = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    total_otp_generated = Column(Integer, default=0)
    otp_verified_count = Column(Integer, default=0)

    def is_valid(self):
        return datetime.utcnow() < self.expires_at
