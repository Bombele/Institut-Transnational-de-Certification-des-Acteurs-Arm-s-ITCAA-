from fastapi import APIRouter, Depends
from pathlib import Path
from apps.api.services.dissemination_service import publish_report, list_public_reports, get_public_report

router = APIRouter(prefix="/dissemination", tags=["dissemination"])

@router.post("/publish")
def publish(year: int, lang: str):
    pdf_path = Path(f"/tmp/annual_report_{year}_{lang}.pdf")
    if not pdf_path.exists():
        return {"error": "report_not_found"}
    uri = publish_report(pdf_path, year, lang)
    return {"message": "Report published", "uri": uri}

@router.get("/list")
def list_reports():
    return list_public_reports()

@router.get("/download/{filename}")
def download_report(filename: str):
    return get_public_report(filename)
