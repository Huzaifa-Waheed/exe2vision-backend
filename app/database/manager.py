from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.models.user import User
from app.models.scan import ScanRecord
from app.models.otp import OTPRecord
from datetime import datetime

class DatabaseManager:

    @staticmethod
    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    # ---------- USER ----------
    @staticmethod
    def get_user_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def create_user(db: Session, name: str, email: str, password_hash: str):
        user = User(name=name, email=email, password_hash=password_hash)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    # ---------- OTP ----------
    @staticmethod
    def save_otp(db: Session, email: str, otp_code: str, expires_minutes=15):
        # create or update OTP entry for this email
        existing = db.query(OTPRecord).filter(OTPRecord.email == email).first()
        expires_at = datetime.utcnow() + timedelta(minutes=expires_minutes)
        if existing:
            existing.otp_code = otp_code
            existing.expires_at = expires_at
            existing.total_otp_generated = (existing.total_otp_generated or 0) + 1
            existing.otp_verified_count = 0
            db.commit()
            db.refresh(existing)
            return existing
        otp = OTPRecord(email=email, otp_code=otp_code, expires_at=expires_at)
        db.add(otp)
        db.commit()
        db.refresh(otp)
        return otp

    @staticmethod
    def get_otp_record(db: Session, email: str):
        return db.query(OTPRecord).filter(OTPRecord.email == email).first()

    @staticmethod
    def verify_and_consume_otp(db: Session, email: str, otp_code: str):
        rec = db.query(OTPRecord).filter(OTPRecord.email == email).first()
        if not rec:
            return False
        if rec.otp_code != otp_code:
            return False
        if not rec.is_valid():
            return False
        rec.otp_verified_count = (rec.otp_verified_count or 0) + 1
        db.commit()
        return True

    @staticmethod
    def update_password(db: Session, email: str, password_hash: str):
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return None
        user.password_hash = password_hash
        db.commit()
        db.refresh(user)
        return user

    # ---------- SCANS ----------
    @staticmethod
    def save_scan(
        db,
        user_id: int,
        filename: str,
        result: str,
        probability: float,
        file_path: str
    ):
        scan = ScanRecord(
            user_id=user_id,
            filename=filename,
            result=result,
            probability=probability,
            file_path=file_path,
            scanned_at=datetime.utcnow()
        )
        db.add(scan)
        db.commit()
        db.refresh(scan)
        return scan

    @staticmethod
    def get_user_scans(db, user_id: int):
        return (
            db.query(ScanRecord)
            .filter(
                ScanRecord.user_id == user_id,
                ScanRecord.is_deleted == False
            )
            .order_by(ScanRecord.scanned_at.desc())
            .all()
        )

    # ---------- ADMIN ----------
    @staticmethod
    def get_all_scans(db):
        return (
            db.query(ScanRecord)
            .filter(ScanRecord.is_deleted == False)
            .order_by(ScanRecord.scanned_at.desc())
            .all()
        )

    @staticmethod
    def soft_delete_scan(db, scan_id: int):
        scan = db.query(ScanRecord).filter(ScanRecord.id == scan_id).first()
        if scan:
            scan.is_deleted = True
            db.commit()
        return scan