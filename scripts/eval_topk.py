#!/usr/bin/env python3
"""Offline evaluator for FastAPI retrieval behavior across top_k variants.

Reads a CSV dataset with a `query` column, calls `/get_response/v1`, and writes:
- raw results per query/top_k
- aggregate metrics per top_k
- comparison summary against baseline top_k
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import statistics
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


@dataclass
class EvalRow:
    query: str
    top_k: int
    http_status: int
    source: str
    fallback_reason: str | None
    latency_ms: int | None
    has_filters: bool
    attribute_count: int
    first_selected_field: str | None
    first_selected_value_number: float | int | None
    first_selected_value_string: str | None
    first_top_similarity: float | None
    first_margin: float | None
    first_selected_score: float | None
    error: str | None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate top_k impact for FastAPI retrieval")
    parser.add_argument("--endpoint", default="http://localhost:8010/get_response/v1", help="FastAPI endpoint")
    parser.add_argument("--dataset", default="scripts/eval_queries_sample.csv", help="CSV file with a 'query' column")
    parser.add_argument("--platform", default="magento")
    parser.add_argument("--tenant-id", default="base")
    parser.add_argument("--locale", default="es_AR")
    parser.add_argument("--store-code", default="default")
    parser.add_argument("--min-similarity", type=float, default=0.30)
    parser.add_argument("--topk-values", default="1,3", help="Comma-separated list, e.g. 1,3")
    parser.add_argument("--timeout", type=float, default=20.0, help="HTTP timeout seconds")
    parser.add_argument("--sleep-ms", type=int, default=0, help="Delay between calls to avoid burst")
    parser.add_argument("--limit", type=int, default=0, help="Optional limit for first N queries")
    parser.add_argument("--out-dir", default="var/evaluation", help="Output folder")
    return parser.parse_args()


def _as_number_or_none(value: Any) -> float | int | None:
    if value is None or value == "":
        return None
    if isinstance(value, (int, float)):
        return value
    try:
        text = str(value)
        if "." in text:
            return float(text)
        return int(text)
    except Exception:
        return None


def load_queries(dataset_path: str, limit: int) -> list[str]:
    queries: list[str] = []
    with open(dataset_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if "query" not in (reader.fieldnames or []):
            raise ValueError("dataset must include a 'query' column")
        for row in reader:
            query = (row.get("query") or "").strip()
            if query:
                queries.append(query)
    if limit > 0:
        return queries[:limit]
    return queries


def fetch_json(url: str, timeout_s: float) -> tuple[int, dict[str, Any] | None, str | None]:
    request = Request(url=url, method="GET")
    try:
        with urlopen(request, timeout=timeout_s) as response:
            raw = response.read().decode("utf-8", errors="replace")
            status = int(response.status)
            try:
                parsed = json.loads(raw)
            except Exception:
                return status, None, "invalid_json"
            if not isinstance(parsed, dict):
                return status, None, "unexpected_payload_type"
            return status, parsed, None
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace") if hasattr(exc, "read") else ""
        return int(exc.code), None, f"http_error:{exc.code}:{body[:300]}"
    except URLError as exc:
        return 0, None, f"url_error:{exc.reason}"
    except Exception as exc:
        return 0, None, f"request_error:{exc}"


def parse_eval_row(query: str, top_k: int, status: int, payload: dict[str, Any] | None, error: str | None) -> EvalRow:
    if payload is None:
        return EvalRow(
            query=query,
            top_k=top_k,
            http_status=status,
            source="error",
            fallback_reason=None,
            latency_ms=None,
            has_filters=False,
            attribute_count=0,
            first_selected_field=None,
            first_selected_value_number=None,
            first_selected_value_string=None,
            first_top_similarity=None,
            first_margin=None,
            first_selected_score=None,
            error=error,
        )

    meta = payload.get("meta") if isinstance(payload.get("meta"), dict) else {}
    retrieval = payload.get("retrieval") if isinstance(payload.get("retrieval"), dict) else {}
    filters = payload.get("filters") if isinstance(payload.get("filters"), list) else []

    attrs = retrieval.get("attributes") if isinstance(retrieval.get("attributes"), list) else []
    first_attr = attrs[0] if attrs and isinstance(attrs[0], dict) else {}
    first_selected = first_attr.get("selected") if isinstance(first_attr.get("selected"), dict) else {}
    first_conf = first_attr.get("confidence") if isinstance(first_attr.get("confidence"), dict) else {}
    first_rerank = first_attr.get("rerank") if isinstance(first_attr.get("rerank"), dict) else {}

    return EvalRow(
        query=query,
        top_k=top_k,
        http_status=status,
        source=str(meta.get("source") or "unknown"),
        fallback_reason=(str(meta.get("fallback_reason")) if meta.get("fallback_reason") is not None else None),
        latency_ms=_as_number_or_none(meta.get("latency_ms")),
        has_filters=len(filters) > 0,
        attribute_count=len(attrs),
        first_selected_field=(str(first_selected.get("attribute_code")) if first_selected.get("attribute_code") is not None else None),
        first_selected_value_number=_as_number_or_none(first_selected.get("attribute_value_number")),
        first_selected_value_string=(str(first_selected.get("attribute_value_string")) if first_selected.get("attribute_value_string") is not None else None),
        first_top_similarity=_as_number_or_none(first_conf.get("top_similarity")),
        first_margin=_as_number_or_none(first_conf.get("margin")),
        first_selected_score=_as_number_or_none(first_rerank.get("selected_score")),
        error=error,
    )


def build_call_url(args: argparse.Namespace, query: str, top_k: int) -> str:
    params = {
        "user_query": query,
        "platform": args.platform,
        "tenant_id": args.tenant_id,
        "locale": args.locale,
        "store_code": args.store_code,
        "top_k": top_k,
        "min_similarity": max(0.0, min(1.0, float(args.min_similarity))),
    }
    return f"{args.endpoint}?{urlencode(params)}"


def aggregate(rows: list[EvalRow]) -> dict[str, Any]:
    by_topk: dict[int, list[EvalRow]] = {}
    for row in rows:
        by_topk.setdefault(row.top_k, []).append(row)

    summary: dict[str, Any] = {}
    for topk, group in sorted(by_topk.items(), key=lambda kv: kv[0]):
        total = len(group)
        ok_rows = [r for r in group if r.error is None and r.http_status == 200]
        latencies = [int(r.latency_ms) for r in ok_rows if isinstance(r.latency_ms, (int, float))]
        margins = [float(r.first_margin) for r in ok_rows if isinstance(r.first_margin, (int, float))]
        similarities = [float(r.first_top_similarity) for r in ok_rows if isinstance(r.first_top_similarity, (int, float))]
        scores = [float(r.first_selected_score) for r in ok_rows if isinstance(r.first_selected_score, (int, float))]

        source_counts: dict[str, int] = {}
        fallback_counts: dict[str, int] = {}
        for r in ok_rows:
            source_counts[r.source] = source_counts.get(r.source, 0) + 1
            if r.fallback_reason:
                fallback_counts[r.fallback_reason] = fallback_counts.get(r.fallback_reason, 0) + 1

        summary[str(topk)] = {
            "queries_total": total,
            "responses_ok": len(ok_rows),
            "errors": total - len(ok_rows),
            "source_counts": source_counts,
            "fallback_reason_counts": fallback_counts,
            "has_filters_rate": round((sum(1 for r in ok_rows if r.has_filters) / len(ok_rows)), 4) if ok_rows else 0.0,
            "avg_latency_ms": round(statistics.mean(latencies), 2) if latencies else None,
            "p95_latency_ms": round(percentile(latencies, 95), 2) if latencies else None,
            "avg_top_similarity": round(statistics.mean(similarities), 4) if similarities else None,
            "avg_margin": round(statistics.mean(margins), 4) if margins else None,
            "avg_selected_score": round(statistics.mean(scores), 4) if scores else None,
        }

    return summary


def percentile(values: list[int], p: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    if len(ordered) == 1:
        return float(ordered[0])
    rank = (p / 100.0) * (len(ordered) - 1)
    lo = int(rank)
    hi = min(lo + 1, len(ordered) - 1)
    frac = rank - lo
    return (ordered[lo] * (1 - frac)) + (ordered[hi] * frac)


def compare_to_baseline(rows: list[EvalRow], baseline_topk: int) -> dict[str, Any]:
    baseline_by_query: dict[str, EvalRow] = {
        row.query: row for row in rows if row.top_k == baseline_topk
    }

    out: dict[str, Any] = {}
    for topk in sorted(set(r.top_k for r in rows)):
        if topk == baseline_topk:
            continue

        changed = 0
        compared = 0
        became_semantic = 0
        became_fallback = 0

        for row in rows:
            if row.top_k != topk:
                continue

            base = baseline_by_query.get(row.query)
            if not base:
                continue
            if row.error is not None or base.error is not None:
                continue
            if row.http_status != 200 or base.http_status != 200:
                continue

            compared += 1
            curr_key = (row.first_selected_field, row.first_selected_value_number, row.first_selected_value_string)
            base_key = (base.first_selected_field, base.first_selected_value_number, base.first_selected_value_string)
            if curr_key != base_key:
                changed += 1

            if base.source != "semantic" and row.source == "semantic":
                became_semantic += 1
            if base.source == "semantic" and row.source == "fallback":
                became_fallback += 1

        out[str(topk)] = {
            "baseline_top_k": baseline_topk,
            "compared_queries": compared,
            "selected_candidate_changed": changed,
            "selected_candidate_changed_rate": round(changed / compared, 4) if compared else 0.0,
            "became_semantic": became_semantic,
            "became_fallback": became_fallback,
        }

    return out


def write_raw_csv(rows: list[EvalRow], path: str) -> None:
    fields = [
        "query",
        "top_k",
        "http_status",
        "source",
        "fallback_reason",
        "latency_ms",
        "has_filters",
        "attribute_count",
        "first_selected_field",
        "first_selected_value_number",
        "first_selected_value_string",
        "first_top_similarity",
        "first_margin",
        "first_selected_score",
        "error",
    ]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({
                "query": row.query,
                "top_k": row.top_k,
                "http_status": row.http_status,
                "source": row.source,
                "fallback_reason": row.fallback_reason,
                "latency_ms": row.latency_ms,
                "has_filters": row.has_filters,
                "attribute_count": row.attribute_count,
                "first_selected_field": row.first_selected_field,
                "first_selected_value_number": row.first_selected_value_number,
                "first_selected_value_string": row.first_selected_value_string,
                "first_top_similarity": row.first_top_similarity,
                "first_margin": row.first_margin,
                "first_selected_score": row.first_selected_score,
                "error": row.error,
            })


def main() -> int:
    args = parse_args()

    topk_values: list[int] = []
    for part in args.topk_values.split(","):
        part = part.strip()
        if not part:
            continue
        try:
            topk = int(part)
        except ValueError as exc:
            raise ValueError(f"invalid top_k value: {part}") from exc
        topk_values.append(max(1, min(5, topk)))

    topk_values = sorted(set(topk_values))
    if not topk_values:
        raise ValueError("topk-values must include at least one integer")

    queries = load_queries(args.dataset, args.limit)
    if not queries:
        raise ValueError("dataset has no valid queries")

    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = os.path.join(args.out_dir, run_id)
    os.makedirs(out_dir, exist_ok=True)

    rows: list[EvalRow] = []

    total_calls = len(queries) * len(topk_values)
    call_i = 0
    for query in queries:
        for topk in topk_values:
            call_i += 1
            url = build_call_url(args, query, topk)
            status, payload, error = fetch_json(url, args.timeout)
            row = parse_eval_row(query, topk, status, payload, error)
            rows.append(row)

            progress = f"[{call_i}/{total_calls}]"
            if row.error is not None:
                print(f"{progress} top_k={topk} query={query!r} ERROR {row.error}")
            else:
                print(
                    f"{progress} top_k={topk} query={query!r} "
                    f"source={row.source} latency_ms={row.latency_ms}"
                )

            if args.sleep_ms > 0:
                time.sleep(args.sleep_ms / 1000.0)

    summary = {
        "run_id": run_id,
        "config": {
            "endpoint": args.endpoint,
            "dataset": args.dataset,
            "platform": args.platform,
            "tenant_id": args.tenant_id,
            "locale": args.locale,
            "store_code": args.store_code,
            "min_similarity": args.min_similarity,
            "topk_values": topk_values,
            "query_count": len(queries),
            "timeout": args.timeout,
        },
        "metrics_by_topk": aggregate(rows),
        "comparison_vs_baseline": compare_to_baseline(rows, baseline_topk=topk_values[0]),
    }

    raw_csv_path = os.path.join(out_dir, "raw_results.csv")
    summary_path = os.path.join(out_dir, "summary.json")

    write_raw_csv(rows, raw_csv_path)
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print("\nEvaluation complete")
    print(f"- summary: {summary_path}")
    print(f"- raw csv: {raw_csv_path}")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
