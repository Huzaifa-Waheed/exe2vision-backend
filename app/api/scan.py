from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.database.manager import DatabaseManager
from app.services.scan_manager import ScanManager
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/scan", tags=["Scan"])

@router.post("/upload")
def upload_and_scan(
    file: UploadFile = File(...),
    db: Session = Depends(DatabaseManager.get_db),
    user = Depends(get_current_user)
):
    scan = ScanManager.process_scan(db, user, file)

    return {
        "message": "Scan completed",
        "scan_result": scan.to_dict()
    }


@router.get("/history")
def scan_history(
    db: Session = Depends(DatabaseManager.get_db),
    user = Depends(get_current_user)
):
    scans = DatabaseManager.get_user_scans(db, user.id)
    return {
        "total": len(scans),
        "history": [scan.to_dict() for scan in scans]
    }
