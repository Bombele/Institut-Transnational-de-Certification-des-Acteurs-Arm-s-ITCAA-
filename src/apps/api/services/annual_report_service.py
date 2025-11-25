from weasyprint import HTML
from pathlib import Path
from fastapi.responses import FileResponse

def render_annual_pdf(html_content: str, year: int):
    pdf_path = Path("/tmp") / f"annual_report_{year}.pdf"
    HTML(string=html_content).write_pdf(str(pdf_path))
    return FileResponse(str(pdf_path), media_type="application/pdf", filename=f"annual_report_{year}.pdf")
