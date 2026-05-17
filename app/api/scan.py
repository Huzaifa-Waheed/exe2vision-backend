from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date
from app.database.manager import DatabaseManager
from app.services.scan_manager import ScanManager
from app.services.report_manager import ReportManager
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/scan", tags=["Scan"])


@router.post("/upload")
def upload_and_scan(
    file: UploadFile = File(...),
    db: Session = Depends(DatabaseManager.get_db),
    user=Depends(get_current_user),
):
    scan = ScanManager.process_scan(db, user, file)
    return {"message": "Scan completed", "scan_result": scan.to_dict()}


@router.get("/history")
def scan_history(
    db: Session = Depends(DatabaseManager.get_db),
    user=Depends(get_current_user),
    result: Optional[str] = Query(None, description="Filter by result: Benign or Malware"),
    from_date: Optional[date] = Query(None),
    to_date: Optional[date] = Query(None),
):
    scans = DatabaseManager.get_user_scans(db, user.id)

    if result:
        scans = [s for s in scans if (s.result or "").lower() == result.lower()]
    if from_date:
        scans = [s for s in scans if s.scanned_at and s.scanned_at.date() >= from_date]
    if to_date:
        scans = [s for s in scans if s.scanned_at and s.scanned_at.date() <= to_date]

    return {"total": len(scans), "history": [s.to_dict() for s in scans]}


@router.get("/report/{scan_id}")
def download_scan_report(
    scan_id: int,
    db: Session = Depends(DatabaseManager.get_db),
    user=Depends(get_current_user),
):
    """Download PDF report for a single scan (FR5.7, FR7.1-7.3)."""
    scans = DatabaseManager.get_user_scans(db, user.id)
    scan = next((s for s in scans if s.id == scan_id), None)
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")

    pdf = ReportManager.generate_scan_pdf(scan)
    return StreamingResponse(
        pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=scan_{scan_id}_report.pdf"},
    )


@router.get("/report")
def download_history_report(
    db: Session = Depends(DatabaseManager.get_db),
    user=Depends(get_current_user),
    result: Optional[str] = Query(None),
    from_date: Optional[date] = Query(None),
    to_date: Optional[date] = Query(None),
):
    """Download overall history PDF report (FR7.4-7.6)."""
    scans = DatabaseManager.get_user_scans(db, user.id)

    if result:
        scans = [s for s in scans if (s.result or "").lower() == result.lower()]
    if from_date:
        scans = [s for s in scans if s.scanned_at and s.scanned_at.date() >= from_date]
    if to_date:
        scans = [s for s in scans if s.scanned_at and s.scanned_at.date() <= to_date]

    pdf = ReportManager.generate_history_pdf(scans)
    return StreamingResponse(
        pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=history_report.pdf"},
    )
