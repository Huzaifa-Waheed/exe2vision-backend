from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO


class ReportManager:

    @staticmethod
    def generate_scan_pdf(scan) -> BytesIO:
        """Single scan PDF report (FR5.7, FR7.2-7.3)."""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        elements = []

        elements.append(Paragraph("Exe2Vision — Scan Report", styles["Title"]))
        elements.append(Spacer(1, 12))

        data = [
            ["Field", "Value"],
            ["Filename", scan.filename or "—"],
            ["Result", scan.result or "—"],
            ["Probability", f"{round((scan.probability or 0) * 100, 2)}%"],
            ["Scanned At", str(scan.scanned_at)],
        ]
        table = Table(data, colWidths=[150, 320])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2d2d2d")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("PADDING", (0, 0), (-1, -1), 8),
        ]))
        elements.append(table)
        doc.build(elements)
        buffer.seek(0)
        return buffer

    @staticmethod
    def generate_history_pdf(scans, title: str = "Scan History Report") -> BytesIO:
        """Overall history PDF report (FR7.4-7.6)."""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        elements = []

        elements.append(Paragraph(f"Exe2Vision — {title}", styles["Title"]))
        elements.append(Paragraph(f"Total scans: {len(scans)}", styles["Normal"]))
        elements.append(Spacer(1, 12))

        data = [["#", "Filename", "Result", "Probability", "Scanned At"]]
        for i, scan in enumerate(scans, 1):
            data.append([
                str(i),
                scan.filename or "—",
                scan.result or "—",
                f"{round((scan.probability or 0) * 100, 2)}%",
                str(scan.scanned_at),
            ])

        table = Table(data, colWidths=[25, 160, 70, 80, 135])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2d2d2d")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("PADDING", (0, 0), (-1, -1), 6),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
        ]))
        elements.append(table)
        doc.build(elements)
        buffer.seek(0)
        return buffer
