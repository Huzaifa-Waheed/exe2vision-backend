from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from datetime import datetime
from app.database.base import Base

class ScanRecord(Base):
    __tablename__ = "scan_records"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    filename = Column(String)
    result = Column(String)
    probability = Column(Float)
    scanned_at = Column(DateTime, default=datetime.utcnow)
    file_path = Column(String)
    is_deleted = Column(Boolean, default=False)

    def to_dict(self):
        return {
            "filename": self.filename,
            "result": self.result,
            "probability": self.probability,
            "scanned_at": self.scanned_at
        }
