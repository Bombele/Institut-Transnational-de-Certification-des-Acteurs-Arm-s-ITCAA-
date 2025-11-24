# apps/api/routers/recognitions.py
router = APIRouter(prefix="/recognitions", tags=["recognitions"])

@router.get("/")
def list_recognitions(org_type: str | None = None, status: str | None = None):
    ...

@router.post("/")
def upsert_recognition(payload: dict):
    ...

# apps/api/routers/advisory.py
router = APIRouter(prefix="/advisory", tags=["advisory"])

@router.get("/members")
def list_members(): ...
@router.get("/resolutions")
def list_resolutions(): ...
