from app.database.session import engine
from app.database.base import Base
from app.models.user import User
from app.models.scan import ScanRecord
from app.models.otp import OTPRecord

def init_db():
    Base.metadata.create_all(bind=engine)
