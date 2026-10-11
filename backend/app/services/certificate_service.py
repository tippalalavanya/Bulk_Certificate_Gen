from pathlib import Path
from uuid import uuid4

from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

from app.core.config import settings


class CertificateService:
    """Render print-ready landscape certificates with a course-aware visual theme."""

    def __init__(self, storage_dir: Path | None = None):
        self.storage_dir = (storage_dir or settings.storage_dir).resolve()
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _theme(course_name: str) -> tuple[colors.Color, colors.Color, colors.Color]:
        palette = (
            (colors.HexColor("#102A43"), colors.HexColor("#2CBFAE"), colors.HexColor("#F4B942")),
            (colors.HexColor("#24143D"), colors.HexColor("#C084FC"), colors.HexColor("#F8D477")),
            (colors.HexColor("#123B4A"), colors.HexColor("#59C3C3"), colors.HexColor("#F6AE2D")),
            (colors.HexColor("#3B1F2B"), colors.HexColor("#E07A5F"), colors.HexColor("#F2CC8F")),
        )
        return palette[sum(ord(char) for char in course_name.lower()) % len(palette)]

    @staticmethod
    def _fit_text(pdf: canvas.Canvas, text: str, font: str, size: float, max_width: float) -> float:
        while size > 10 and stringWidth(text, font, size) > max_width:
            size -= 1
        return size

    def generate(self, *, name: str, course_name: str, issue_date: str, organization: str, footer: str) -> tuple[str, str]:
        certificate_id = str(uuid4())
        key = f"{certificate_id}.pdf"
        destination = (self.storage_dir / key).resolve()
        if destination.parent != self.storage_dir:
            raise ValueError("unsafe storage path")
        temporary = destination.with_suffix(".tmp")
        try:
            width, height = landscape(A4)
            primary, accent, gold = self._theme(course_name)
            pdf = canvas.Canvas(str(temporary), pagesize=(width, height))
            pdf.setTitle(f"Certificate {certificate_id}")
            pdf.setFillColor(colors.white)
            pdf.rect(0, 0, width, height, fill=1, stroke=0)
            pdf.setFillColor(primary)
            pdf.rect(0, 0, 118, height, fill=1, stroke=0)
            pdf.setFillColor(accent)
            pdf.circle(59, height - 73, 27, fill=1, stroke=0)
            pdf.setFillColor(colors.white)
            pdf.setFont("Helvetica-Bold", 20)
            pdf.drawCentredString(59, height - 80, "C")
            pdf.setFont("Helvetica-Bold", 9)
            pdf.drawCentredString(59, 45, "CERTIFY")
            pdf.setStrokeColor(gold)
            pdf.setLineWidth(2)
            pdf.rect(24, 24, width - 48, height - 48, fill=0, stroke=1)
            pdf.setStrokeColor(primary)
            pdf.setLineWidth(0.7)
            pdf.rect(138, 42, width - 180, height - 84, fill=0, stroke=1)
            center = (width + 118) / 2
            pdf.setFillColor(primary)
            pdf.setFont("Helvetica-Bold", 25)
            pdf.drawCentredString(center, height - 105, "CERTIFICATE OF COMPLETION")
            pdf.setFillColor(accent)
            pdf.setFont("Helvetica-Bold", 9)
            pdf.drawCentredString(center, height - 127, "PROUDLY PRESENTED WITH DISTINCTION")
            pdf.setFillColor(colors.HexColor("#5B6675"))
            pdf.setFont("Helvetica", 13)
            pdf.drawCentredString(center, height - 177, "This certificate is awarded to")
            name_size = self._fit_text(pdf, name, "Helvetica-Bold", 32, width - 270)
            pdf.setFillColor(primary)
            pdf.setFont("Helvetica-Bold", name_size)
            pdf.drawCentredString(center, height - 225, name)
            pdf.setStrokeColor(accent)
            pdf.setLineWidth(1.4)
            pdf.line(center - 105, height - 244, center + 105, height - 244)
            pdf.setFillColor(colors.HexColor("#5B6675"))
            pdf.setFont("Helvetica", 13)
            pdf.drawCentredString(center, height - 280, "for successfully completing")
            course_size = self._fit_text(pdf, course_name, "Helvetica-Bold", 22, width - 280)
            pdf.setFillColor(primary)
            pdf.setFont("Helvetica-Bold", course_size)
            pdf.drawCentredString(center, height - 316, course_name)
            pdf.setFillColor(colors.HexColor("#5B6675"))
            pdf.setFont("Helvetica", 10)
            pdf.drawCentredString(center, 91, f"Issued {issue_date}  ·  Certificate ID {certificate_id}")
            pdf.setFillColor(primary)
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawCentredString(center, 70, organization)
            if footer:
                pdf.setFillColor(colors.HexColor("#718096"))
                pdf.setFont("Helvetica-Oblique", 9)
                pdf.drawCentredString(center, 53, footer)
            pdf.save()
            temporary.replace(destination)
            return certificate_id, key
        except Exception:
            temporary.unlink(missing_ok=True)
            destination.unlink(missing_ok=True)
            raise
