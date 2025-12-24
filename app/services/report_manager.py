from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO

class ReportManager:

    def generate_pdf(self, scan):
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)

        c.drawString(100, 800, f"File: {scan.filename}")
        c.drawString(100, 780, f"Result: {scan.result}")
        c.drawString(100, 760, f"Probability: {scan.probability}")

        c.showPage()
        c.save()
        buffer.seek(0)
        return buffer
