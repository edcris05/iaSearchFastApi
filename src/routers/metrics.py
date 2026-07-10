from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import PlainTextResponse

from src.models.contracts import SearchEventIn
from src.models.search_event import SearchEventRepository
from src.utils.auth import require_admin_api_key


metrics_router = APIRouter(dependencies=[Depends(require_admin_api_key)])


def _parse_iso_dt(value: str) -> datetime:
    try:
        return datetime.fromisoformat(value)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"invalid_datetime:{value}") from exc


@metrics_router.post("/event", tags=["Metrics"])
def log_event(payload: SearchEventIn):
    repo = SearchEventRepository()
    ok = repo.log_event(payload.model_dump())
    return {"ok": ok}


@metrics_router.get("/summary", tags=["Metrics"])
def summary(
    platform: str = Query(...),
    tenant_id: str = Query(...),
    from_dt: str = Query(..., alias="from"),
    to_dt: str = Query(..., alias="to"),
):
    repo = SearchEventRepository()
    return repo.export_metrics_summary(
        platform=platform,
        tenant_id=tenant_id,
        from_dt=_parse_iso_dt(from_dt),
        to_dt=_parse_iso_dt(to_dt),
    )


@metrics_router.get("/export", tags=["Metrics"])
def export_csv(
    platform: str = Query(...),
    tenant_id: str = Query(...),
    from_dt: str = Query(..., alias="from"),
    to_dt: str = Query(..., alias="to"),
):
    repo = SearchEventRepository()
    csv_body = repo.export_events_csv(
        platform=platform,
        tenant_id=tenant_id,
        from_dt=_parse_iso_dt(from_dt),
        to_dt=_parse_iso_dt(to_dt),
    )
    return PlainTextResponse(content=csv_body, media_type="text/csv")
