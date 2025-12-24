from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database.base import Base
from app.core.security import verify_password

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(String, default="user")
    created_at = Column(DateTime, default=datetime.utcnow)

    def verify_password(self, pwd: str) -> bool:
        return verify_password(pwd, self.password_hash)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email, "role": self.role}
