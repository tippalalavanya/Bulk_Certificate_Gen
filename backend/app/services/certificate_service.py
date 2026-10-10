from pathlib import Path
from uuid import uuid4
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from app.core.config import settings

class CertificateService:
    def __init__(self, storage_dir: Path | None = None):
        self.storage_dir = (storage_dir or settings.storage_dir).resolve()
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def generate(self, *, name: str, course_name: str, issue_date: str, organization: str, footer: str) -> tuple[str, str]:
        certificate_id = str(uuid4())
        key = f"{certificate_id}.pdf"
        destination = (self.storage_dir / key).resolve()
        if destination.parent != self.storage_dir: raise ValueError("unsafe storage path")
        temporary = destination.with_suffix(".tmp")
        try:
            pdf = canvas.Canvas(str(temporary), pagesize=A4)
            width, height = A4
            pdf.setTitle(f"Certificate {certificate_id}")
            pdf.setStrokeColorRGB(0.12, 0.32, 0.45); pdf.rect(42, 42, width-84, height-84)
            pdf.setFillColorRGB(0.12, 0.32, 0.45); pdf.setFont("Helvetica-Bold", 27); pdf.drawCentredString(width/2, height-160, "CERTIFICATE OF COMPLETION")
            pdf.setFillColorRGB(0.15, 0.15, 0.15); pdf.setFont("Helvetica", 13); pdf.drawCentredString(width/2, height-220, "This certificate is proudly presented to")
            pdf.setFont("Helvetica-Bold", 26); pdf.drawCentredString(width/2, height-275, name)
            pdf.setFont("Helvetica", 14); pdf.drawCentredString(width/2, height-330, "for successfully completing")
            pdf.setFont("Helvetica-Bold", 19); pdf.drawCentredString(width/2, height-370, course_name)
            pdf.setFont("Helvetica", 12); pdf.drawCentredString(width/2, 150, f"Issued on {issue_date}  •  Certificate ID: {certificate_id}")
            pdf.setFont("Helvetica-Bold", 12); pdf.drawCentredString(width/2, 112, organization)
            pdf.setFont("Helvetica-Oblique", 10); pdf.drawCentredString(width/2, 88, footer)
            pdf.save(); temporary.replace(destination)
            return certificate_id, key
        except Exception:
            temporary.unlink(missing_ok=True); destination.unlink(missing_ok=True); raise
