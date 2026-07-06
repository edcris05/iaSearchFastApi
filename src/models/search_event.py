import csv
import io
import json
from datetime import datetime
from typing import Any

from src.models.generic_postgresql import GenericPostgresql


class SearchEventRepository(GenericPostgresql):
    def log_event(self, payload: dict[str, Any]) -> bool:
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO search_events (
                        request_id, platform, tenant_id, session_id, event_type,
                        query_text, source, fallback_reason, api_version, latency_ms,
                        filters, product_id, position
                    ) VALUES (
                        %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s,
                        %s::jsonb, %s, %s
                    )
                    """,
                    (
                        payload["request_id"],
                        payload["platform"],
                        payload["tenant_id"],
                        payload.get("session_id"),
                        payload["event_type"],
                        payload.get("query_text"),
                        payload.get("source"),
                        payload.get("fallback_reason"),
                        payload.get("api_version"),
                        payload.get("latency_ms"),
                        json.dumps(payload.get("filters", [])),
                        payload.get("product_id"),
                        payload.get("position"),
                    ),
                )
                conn.commit()
                return True
        finally:
            conn.close()

    def _build_where(self, platform: str, tenant_id: str, from_dt: datetime, to_dt: datetime):
        return (
            "WHERE platform = %s AND tenant_id = %s AND created_at >= %s AND created_at <= %s",
            (platform, tenant_id, from_dt, to_dt),
        )

    def export_metrics_summary(self, platform: str, tenant_id: str, from_dt: datetime, to_dt: datetime) -> dict[str, Any]:
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                where_sql, params = self._build_where(platform, tenant_id, from_dt, to_dt)

                cursor.execute(
                    f"""
                    SELECT
                      count(*) FILTER (WHERE event_type = 'search') AS total_searches,
                      count(*) FILTER (WHERE event_type = 'result_click') AS total_clicks,
                      count(*) FILTER (WHERE event_type = 'add_to_cart') AS total_add_to_cart,
                      count(*) FILTER (WHERE event_type = 'conversion') AS total_conversions,
                      avg(latency_ms) FILTER (WHERE event_type = 'search') AS avg_latency_ms
                    FROM search_events
                    {where_sql}
                    """,
                    params,
                )
                row = cursor.fetchone()

                total_searches = int(row[0] or 0)
                total_clicks = int(row[1] or 0)
                total_add_to_cart = int(row[2] or 0)
                total_conversions = int(row[3] or 0)
                avg_latency = float(row[4] or 0)

                cursor.execute(
                    f"""
                    SELECT source, count(*)
                    FROM search_events
                    {where_sql} AND event_type = 'search'
                    GROUP BY source
                    ORDER BY count(*) DESC
                    """,
                    params,
                )
                sources = [{"source": r[0], "count": int(r[1])} for r in cursor.fetchall()]

                cursor.execute(
                    f"""
                    SELECT fallback_reason, count(*)
                    FROM search_events
                    {where_sql} AND event_type = 'search' AND fallback_reason IS NOT NULL
                    GROUP BY fallback_reason
                    ORDER BY count(*) DESC
                    """,
                    params,
                )
                fallback_reasons = [{"fallback_reason": r[0], "count": int(r[1])} for r in cursor.fetchall()]

                ctr = (total_clicks / total_searches) if total_searches > 0 else 0.0
                atc_rate = (total_add_to_cart / total_searches) if total_searches > 0 else 0.0
                conv_rate = (total_conversions / total_searches) if total_searches > 0 else 0.0

                return {
                    "platform": platform,
                    "tenant_id": tenant_id,
                    "from": from_dt.isoformat(),
                    "to": to_dt.isoformat(),
                    "total_searches": total_searches,
                    "total_clicks": total_clicks,
                    "total_add_to_cart": total_add_to_cart,
                    "total_conversions": total_conversions,
                    "avg_latency_ms": round(avg_latency, 2),
                    "ctr": round(ctr, 4),
                    "add_to_cart_rate": round(atc_rate, 4),
                    "conversion_rate": round(conv_rate, 4),
                    "sources_breakdown": sources,
                    "fallback_reasons": fallback_reasons,
                }
        finally:
            conn.close()

    def export_events_csv(self, platform: str, tenant_id: str, from_dt: datetime, to_dt: datetime) -> str:
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                where_sql, params = self._build_where(platform, tenant_id, from_dt, to_dt)
                cursor.execute(
                    f"""
                    SELECT request_id, event_type, query_text, source, fallback_reason,
                           api_version, latency_ms, product_id, position, created_at
                    FROM search_events
                    {where_sql}
                    ORDER BY created_at ASC
                    """,
                    params,
                )
                rows = cursor.fetchall()

                out = io.StringIO()
                writer = csv.writer(out)
                writer.writerow([
                    "request_id",
                    "event_type",
                    "query_text",
                    "source",
                    "fallback_reason",
                    "api_version",
                    "latency_ms",
                    "product_id",
                    "position",
                    "created_at",
                ])
                for row in rows:
                    writer.writerow(list(row))
                return out.getvalue()
        finally:
            conn.close()
