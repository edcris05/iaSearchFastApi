import json
import re
from dataclasses import dataclass
from typing import Any

import psycopg

from src.models.generic_postgresql import GenericPostgresql
from src.utils.scope_config import DEFAULT_LOCALE


@dataclass
class AppliedCorrection:
    correction_id: int
    attribute_code: str
    raw_phrase: str
    old_value_string: str
    old_value_number: Any
    new_value_string: str
    new_value_number: Any
    rule_type: str
    priority: int


class DuplicateActiveCorrectionError(Exception):
    def __init__(self, existing_id: int | None = None):
        super().__init__("duplicate_active_correction")
        self.existing_id = existing_id


class CorrectionsRepository(GenericPostgresql):
    def _normalize(self, value: Any) -> str:
        if value is None:
            return ""
        return str(value).strip().lower()

    def list_corrections(
        self,
        platform: str,
        tenant_id: str,
        locale: str,
        attribute_code: str | None = None,
        include_inactive: bool = False,
    ) -> list[dict[str, Any]]:
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                query = """
                    SELECT id, platform, tenant_id, locale, attribute_code,
                           raw_phrase, corrected_value_string, corrected_value_number,
                           rule_type, priority, is_active, created_by, created_at, updated_at
                    FROM corrections
                    WHERE platform = %s
                      AND tenant_id = %s
                      AND locale = %s
                """
                params: list[Any] = [platform, tenant_id, locale]

                if attribute_code:
                    query += " AND attribute_code = %s"
                    params.append(attribute_code)

                if not include_inactive:
                    query += " AND is_active = true"

                query += " ORDER BY priority ASC, id ASC"
                cursor.execute(query, tuple(params))
                rows = cursor.fetchall()

                out: list[dict[str, Any]] = []
                for row in rows:
                    out.append(
                        {
                            "id": row[0],
                            "platform": row[1],
                            "tenant_id": row[2],
                            "locale": row[3],
                            "attribute_code": row[4],
                            "raw_phrase": row[5],
                            "corrected_value_string": row[6],
                            "corrected_value_number": row[7],
                            "rule_type": row[8],
                            "priority": row[9],
                            "is_active": row[10],
                            "created_by": row[11],
                            "created_at": row[12],
                            "updated_at": row[13],
                        }
                    )

                return out
        finally:
            conn.close()

    def _write_audit(
        self,
        correction_id: int | None,
        action: str,
        old_data: dict[str, Any] | None,
        new_data: dict[str, Any] | None,
        changed_by: str,
    ) -> None:
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO corrections_audit (correction_id, action, old_data, new_data, changed_by)
                    VALUES (%s, %s, %s::jsonb, %s::jsonb, %s)
                    """,
                    (
                        correction_id,
                        action,
                        json.dumps(old_data, default=str) if old_data is not None else None,
                        json.dumps(new_data, default=str) if new_data is not None else None,
                        changed_by,
                    ),
                )
                conn.commit()
        finally:
            conn.close()

    def _find_active_duplicate_id(
        self,
        cursor,
        platform: str,
        tenant_id: str,
        locale: str,
        attribute_code: str,
        raw_phrase: str,
        exclude_id: int | None = None,
    ) -> int | None:
        query = """
            SELECT id
            FROM corrections
            WHERE platform = %s
              AND tenant_id = %s
              AND locale = %s
              AND attribute_code = %s
              AND lower(btrim(raw_phrase)) = lower(btrim(%s))
              AND is_active = true
        """
        params: list[Any] = [platform, tenant_id, locale, attribute_code, raw_phrase]

        if exclude_id is not None:
            query += " AND id <> %s"
            params.append(exclude_id)

        query += " LIMIT 1"
        cursor.execute(query, tuple(params))
        row = cursor.fetchone()
        if row is None:
            return None
        return int(row[0])

    def create_correction(self, payload: dict[str, Any]) -> dict[str, Any]:
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                platform = payload["platform"]
                tenant_id = payload["tenant_id"]
                locale = payload.get("locale", DEFAULT_LOCALE)
                attribute_code = payload["attribute_code"]
                raw_phrase = payload["raw_phrase"]
                is_active = payload.get("is_active", True)

                if is_active:
                    duplicate_id = self._find_active_duplicate_id(
                        cursor=cursor,
                        platform=platform,
                        tenant_id=tenant_id,
                        locale=locale,
                        attribute_code=attribute_code,
                        raw_phrase=raw_phrase,
                    )
                    if duplicate_id is not None:
                        raise DuplicateActiveCorrectionError(existing_id=duplicate_id)

                cursor.execute(
                    """
                    INSERT INTO corrections (
                        platform, tenant_id, locale, attribute_code,
                        raw_phrase, corrected_value_string, corrected_value_number,
                        rule_type, priority, is_active, created_by
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id, platform, tenant_id, locale, attribute_code,
                              raw_phrase, corrected_value_string, corrected_value_number,
                              rule_type, priority, is_active, created_by, created_at, updated_at
                    """,
                    (
                        platform,
                        tenant_id,
                        locale,
                        attribute_code,
                        raw_phrase,
                        payload.get("corrected_value_string", ""),
                        payload.get("corrected_value_number"),
                        payload.get("rule_type", "exact"),
                        payload.get("priority", 100),
                        is_active,
                        payload.get("created_by", "system"),
                    ),
                )
                row = cursor.fetchone()
                conn.commit()

                created = {
                    "id": row[0],
                    "platform": row[1],
                    "tenant_id": row[2],
                    "locale": row[3],
                    "attribute_code": row[4],
                    "raw_phrase": row[5],
                    "corrected_value_string": row[6],
                    "corrected_value_number": row[7],
                    "rule_type": row[8],
                    "priority": row[9],
                    "is_active": row[10],
                    "created_by": row[11],
                    "created_at": row[12],
                    "updated_at": row[13],
                }

                self._write_audit(
                    correction_id=created["id"],
                    action="insert",
                    old_data=None,
                    new_data=created,
                    changed_by=created["created_by"],
                )
                return created
        except psycopg.errors.UniqueViolation:
            conn.rollback()
            raise DuplicateActiveCorrectionError()
        finally:
            conn.close()

    def update_correction(self, correction_id: int, payload: dict[str, Any], changed_by: str) -> dict[str, Any] | None:
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, platform, tenant_id, locale, attribute_code,
                           raw_phrase, corrected_value_string, corrected_value_number,
                           rule_type, priority, is_active, created_by, created_at, updated_at
                    FROM corrections
                    WHERE id = %s
                    """,
                    (correction_id,),
                )
                old_row = cursor.fetchone()
                if old_row is None:
                    return None

                old_data = {
                    "id": old_row[0],
                    "platform": old_row[1],
                    "tenant_id": old_row[2],
                    "locale": old_row[3],
                    "attribute_code": old_row[4],
                    "raw_phrase": old_row[5],
                    "corrected_value_string": old_row[6],
                    "corrected_value_number": old_row[7],
                    "rule_type": old_row[8],
                    "priority": old_row[9],
                    "is_active": old_row[10],
                    "created_by": old_row[11],
                    "created_at": old_row[12],
                    "updated_at": old_row[13],
                }

                effective_locale = payload.get("locale", old_data["locale"])
                effective_attribute_code = payload.get("attribute_code", old_data["attribute_code"])
                effective_raw_phrase = payload.get("raw_phrase", old_data["raw_phrase"])
                effective_is_active = payload.get("is_active", old_data["is_active"])

                if effective_is_active:
                    duplicate_id = self._find_active_duplicate_id(
                        cursor=cursor,
                        platform=old_data["platform"],
                        tenant_id=old_data["tenant_id"],
                        locale=effective_locale,
                        attribute_code=effective_attribute_code,
                        raw_phrase=effective_raw_phrase,
                        exclude_id=correction_id,
                    )
                    if duplicate_id is not None:
                        raise DuplicateActiveCorrectionError(existing_id=duplicate_id)

                cursor.execute(
                    """
                    UPDATE corrections
                    SET locale = COALESCE(%s, locale),
                        attribute_code = COALESCE(%s, attribute_code),
                        raw_phrase = COALESCE(%s, raw_phrase),
                        corrected_value_string = COALESCE(%s, corrected_value_string),
                        corrected_value_number = %s,
                        rule_type = COALESCE(%s, rule_type),
                        priority = COALESCE(%s, priority),
                        is_active = COALESCE(%s, is_active),
                        updated_at = now()
                    WHERE id = %s
                    RETURNING id, platform, tenant_id, locale, attribute_code,
                              raw_phrase, corrected_value_string, corrected_value_number,
                              rule_type, priority, is_active, created_by, created_at, updated_at
                    """,
                    (
                        payload.get("locale"),
                        payload.get("attribute_code"),
                        payload.get("raw_phrase"),
                        payload.get("corrected_value_string"),
                        payload.get("corrected_value_number", old_data["corrected_value_number"]),
                        payload.get("rule_type"),
                        payload.get("priority"),
                        payload.get("is_active"),
                        correction_id,
                    ),
                )
                row = cursor.fetchone()
                conn.commit()

                new_data = {
                    "id": row[0],
                    "platform": row[1],
                    "tenant_id": row[2],
                    "locale": row[3],
                    "attribute_code": row[4],
                    "raw_phrase": row[5],
                    "corrected_value_string": row[6],
                    "corrected_value_number": row[7],
                    "rule_type": row[8],
                    "priority": row[9],
                    "is_active": row[10],
                    "created_by": row[11],
                    "created_at": row[12],
                    "updated_at": row[13],
                }

                self._write_audit(
                    correction_id=correction_id,
                    action="update",
                    old_data=old_data,
                    new_data=new_data,
                    changed_by=changed_by,
                )
                return new_data
        except psycopg.errors.UniqueViolation:
            conn.rollback()
            raise DuplicateActiveCorrectionError()
        finally:
            conn.close()

    def deactivate_correction(self, correction_id: int, changed_by: str) -> bool:
        updated = self.update_correction(correction_id, {"is_active": False}, changed_by)
        if updated is None:
            return False
        self._write_audit(
            correction_id=correction_id,
            action="delete",
            old_data=None,
            new_data={"is_active": False},
            changed_by=changed_by,
        )
        return True

    def _matches(self, rule_type: str, raw_phrase: str, query_text: str, phrase: str, value_string: str) -> bool:
        raw = self._normalize(raw_phrase)
        if raw == "":
            return False

        haystacks = [
            self._normalize(query_text),
            self._normalize(phrase),
            self._normalize(value_string),
        ]

        if rule_type == "exact":
            return any(h == raw for h in haystacks)

        if rule_type == "contains":
            return any(raw in h for h in haystacks if h != "")

        if rule_type == "regex":
            try:
                return any(re.search(raw_phrase, h, re.IGNORECASE) is not None for h in haystacks if h != "")
            except re.error:
                return False

        return False

    def apply_corrections(
        self,
        filters: list,
        query_text: str,
        platform: str,
        tenant_id: str,
        locale: str = DEFAULT_LOCALE,
    ) -> tuple[list, list[dict[str, Any]]]:
        if not isinstance(filters, list) or not filters:
            return filters, []

        active_rules = self.list_corrections(
            platform=platform,
            tenant_id=tenant_id,
            locale=locale,
            include_inactive=False,
        )

        if not active_rules:
            return filters, []

        rules_by_attr: dict[str, list[dict[str, Any]]] = {}
        for rule in active_rules:
            attr = str(rule.get("attribute_code", "")).strip()
            if attr == "":
                continue
            rules_by_attr.setdefault(attr, []).append(rule)

        for attr_rules in rules_by_attr.values():
            attr_rules.sort(key=lambda r: (int(r.get("priority", 100)), int(r.get("id", 0))))

        applied: list[dict[str, Any]] = []
        out_filters: list = []

        for group in filters:
            if not isinstance(group, list):
                continue

            out_group = []
            for candidate in group:
                if not isinstance(candidate, list) or len(candidate) < 5:
                    continue

                field = str(candidate[0]).strip()
                value_string = "" if candidate[1] is None else str(candidate[1]).strip()
                value_number = candidate[2]
                phrase = "" if candidate[3] is None else str(candidate[3]).strip()
                similarity = candidate[4]

                matched_rule = None
                for rule in rules_by_attr.get(field, []):
                    if self._matches(
                        rule_type=str(rule.get("rule_type", "exact")),
                        raw_phrase=str(rule.get("raw_phrase", "")),
                        query_text=query_text,
                        phrase=phrase,
                        value_string=value_string,
                    ):
                        matched_rule = rule
                        break

                if matched_rule is None:
                    out_group.append([field, value_string, value_number, phrase, similarity])
                    continue

                new_value_string = matched_rule.get("corrected_value_string")
                new_value_number = matched_rule.get("corrected_value_number")

                if new_value_string is None:
                    new_value_string = ""

                out_group.append([
                    field,
                    str(new_value_string),
                    new_value_number,
                    phrase,
                    similarity,
                ])

                applied.append(
                    {
                        "correction_id": int(matched_rule["id"]),
                        "attribute_code": field,
                        "raw_phrase": str(matched_rule.get("raw_phrase", "")),
                        "old_value_string": value_string,
                        "old_value_number": value_number,
                        "new_value_string": str(new_value_string),
                        "new_value_number": new_value_number,
                        "rule_type": str(matched_rule.get("rule_type", "exact")),
                        "priority": int(matched_rule.get("priority", 100)),
                    }
                )

            if out_group:
                out_filters.append(out_group)

        return out_filters, applied
