from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.manager import DatabaseManager
from app.schemas.admin import DeleteScansSchema

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

@router.delete("/scans")
def delete_selected_scans(
    data: DeleteScansSchema,
    db: Session = Depends(DatabaseManager.get_db)
):
    if not data.ids:
        raise HTTPException(status_code=400, detail="No scan ids provided")
    deleted_count = DatabaseManager.soft_delete_scans(db, data.ids)
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="No matching scans found to delete")
    return {"message": f"{deleted_count} scans deleted successfully"}

@router.delete("/scans/all")
def delete_all_scans(
    db: Session = Depends(DatabaseManager.get_db)
):
    deleted_count = DatabaseManager.soft_delete_all_scans(db)
    return {"message": f"{deleted_count} scans deleted successfully"}
