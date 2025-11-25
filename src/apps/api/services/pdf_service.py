from weasyprint import HTML
from fastapi.responses import FileResponse
from pathlib import Path

def render_pdf(html_content: str, filename: str = "report.pdf"):
    pdf_path = Path("/tmp") / filename
    HTML(string=html_content).write_pdf(str(pdf_path))
    return FileResponse(str(pdf_path), media_type="application/pdf", filename=filename)
