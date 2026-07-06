from fastapi import APIRouter, HTTPException, Query

from src.models.contracts import CorrectionCreate, CorrectionUpdate
from src.models.corrections import CorrectionsRepository, DuplicateActiveCorrectionError


corrections_router = APIRouter()


@corrections_router.get("/", tags=["Corrections"])
def list_corrections(
    platform: str = Query(...),
    tenant_id: str = Query(...),
    locale: str = Query("es_AR"),
    attribute_code: str | None = Query(default=None),
    include_inactive: bool = Query(default=False),
):
    repo = CorrectionsRepository()
    return repo.list_corrections(
        platform=platform,
        tenant_id=tenant_id,
        locale=locale,
        attribute_code=attribute_code,
        include_inactive=include_inactive,
    )


@corrections_router.post("/", tags=["Corrections"])
def create_correction(payload: CorrectionCreate):
    repo = CorrectionsRepository()
    try:
        created = repo.create_correction(payload.model_dump())
    except DuplicateActiveCorrectionError as exc:
        raise HTTPException(
            status_code=409,
            detail={
                "code": "duplicate_active_correction",
                "existing_id": exc.existing_id,
            },
        ) from exc
    return {"ok": True, "correction": created}


@corrections_router.put("/{correction_id}", tags=["Corrections"])
def update_correction(correction_id: int, payload: CorrectionUpdate):
    repo = CorrectionsRepository()
    body = payload.model_dump(exclude_none=True)
    changed_by = body.pop("changed_by", "system")
    try:
        updated = repo.update_correction(correction_id=correction_id, payload=body, changed_by=changed_by)
    except DuplicateActiveCorrectionError as exc:
        raise HTTPException(
            status_code=409,
            detail={
                "code": "duplicate_active_correction",
                "existing_id": exc.existing_id,
            },
        ) from exc
    if updated is None:
        raise HTTPException(status_code=404, detail="correction_not_found")
    return {"ok": True, "correction": updated}


@corrections_router.delete("/{correction_id}", tags=["Corrections"])
def delete_correction(correction_id: int, changed_by: str = Query(default="system")):
    repo = CorrectionsRepository()
    ok = repo.deactivate_correction(correction_id=correction_id, changed_by=changed_by)
    if not ok:
        raise HTTPException(status_code=404, detail="correction_not_found")
    return {"ok": True}
