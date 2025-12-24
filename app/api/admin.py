from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.manager import DatabaseManager

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/scans")
def view_all_scans(
    db: Session = Depends(DatabaseManager.get_db)
):
    scans = DatabaseManager.get_all_scans(db)
    return {
        "total": len(scans),
        "scans": [scan.to_dict() for scan in scans]
    }

@router.delete("/scan/{scan_id}")
def delete_scan(
    scan_id: int,
    db: Session = Depends(DatabaseManager.get_db)
):
    scan = DatabaseManager.soft_delete_scan(db, scan_id)
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")

    return {"message": "Scan deleted successfully"}
