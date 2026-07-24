import json
import os
import re
import unicodedata
from dataclasses import dataclass
from typing import Any


@dataclass
class RedirectMatch:
    url: str
    match_type: str
    priority: int
    matched_phrase: str
    query_used: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "url": self.url,
            "match_type": self.match_type,
            "priority": self.priority,
            "matched_phrase": self.matched_phrase,
            "query_used": self.query_used,
        }


class QueryRulesResolver:
    """
    Resuelve stopwords y redirects por scope multi-commerce.

    Env vars soportadas:
    - QUERY_RULES_JSON
    - QUERY_RULES_JSON__<PLATFORM>
    - QUERY_RULES_JSON__<PLATFORM>__<TENANT>
    - QUERY_RULES_JSON__<PLATFORM>__<TENANT>__<LOCALE>
    - QUERY_RULES_JSON__<PLATFORM>__<TENANT>__<LOCALE>__<STORE>
    """

    def _scope_part(self, value: str | None) -> str:
        text = "" if value is None else str(value).strip().lower()
        if text == "":
            return "DEFAULT"
        normalized = "".join(ch if ch.isalnum() else "_" for ch in text)
        while "__" in normalized:
            normalized = normalized.replace("__", "_")
        normalized = normalized.strip("_")
        return normalized.upper() if normalized != "" else "DEFAULT"

    def _scoped_env_names(
        self,
        base: str,
        platform: str,
        tenant_id: str,
        locale: str,
        store_code: str,
    ) -> list[str]:
        p = self._scope_part(platform)
        t = self._scope_part(tenant_id)
        l = self._scope_part(locale)
        s = self._scope_part(store_code)

        return [
            f"{base}__{p}",
            f"{base}__{p}__{t}",
            f"{base}__{p}__{t}__{l}",
            f"{base}__{p}__{t}__{l}__{s}",
        ]

    def _normalize_text(self, text: str) -> str:
        if text is None:
            return ""
        value = str(text).strip().lower()
        value = unicodedata.normalize("NFKD", value)
        value = "".join(ch for ch in value if not unicodedata.combining(ch))
        value = re.sub(r"\s+", " ", value)
        return value.strip()

    def _load_scoped_config(
        self,
        platform: str,
        tenant_id: str,
        locale: str,
        store_code: str,
    ) -> dict[str, Any]:
        raw = os.getenv("QUERY_RULES_JSON", "").strip()

        for env_name in self._scoped_env_names(
            base="QUERY_RULES_JSON",
            platform=platform,
            tenant_id=tenant_id,
            locale=locale,
            store_code=store_code,
        ):
            scoped_raw = os.getenv(env_name, "").strip()
            if scoped_raw != "":
                raw = scoped_raw

        if raw == "":
            return {}

        try:
            parsed = json.loads(raw)
            return parsed if isinstance(parsed, dict) else {}
        except Exception:
            return {}

    def _extract_stopwords(self, config: dict[str, Any]) -> list[str]:
        stopwords_raw = config.get("stopwords", [])
        if not isinstance(stopwords_raw, list):
            return []

        stopwords = []
        for item in stopwords_raw:
            value = self._normalize_text(str(item))
            if value != "":
                stopwords.append(value)

        return list(dict.fromkeys(stopwords))

    def _extract_redirects(self, config: dict[str, Any]) -> list[dict[str, Any]]:
        redirects_raw = config.get("redirects", [])
        if not isinstance(redirects_raw, list):
            return []

        rules: list[dict[str, Any]] = []
        for row in redirects_raw:
            if not isinstance(row, dict):
                continue

            phrases = row.get("phrases", [])
            if not isinstance(phrases, list):
                continue

            clean_phrases = []
            for phrase in phrases:
                value = self._normalize_text(str(phrase))
                if value != "":
                    clean_phrases.append(value)

            if not clean_phrases:
                continue

            url = str(row.get("url", "")).strip()
            if url == "":
                continue

            match_type = self._normalize_text(str(row.get("match", "contains")))
            if match_type not in ["contains", "equals", "regex"]:
                match_type = "contains"

            try:
                priority = int(row.get("priority", 0))
            except Exception:
                priority = 0

            rules.append(
                {
                    "phrases": clean_phrases,
                    "url": url,
                    "match": match_type,
                    "priority": priority,
                }
            )

        rules.sort(key=lambda x: int(x.get("priority", 0)), reverse=True)
        return rules

    def apply_stopwords(self, query: str, stopwords: list[str]) -> tuple[str, list[str]]:
        query_text = "" if query is None else str(query).strip()
        if query_text == "" or not stopwords:
            return query_text, []

        tokens = re.split(r"[\s,.;:+\-/()\[\]{}!?¿¡\"']+", query_text)
        kept: list[str] = []
        removed: list[str] = []

        stopword_set = set(stopwords)
        for token in tokens:
            value = token.strip()
            if value == "":
                continue
            normalized = self._normalize_text(value)
            if normalized in stopword_set:
                removed.append(normalized)
                continue
            kept.append(value)

        cleaned = " ".join(kept).strip()
        if cleaned == "":
            return query_text, list(dict.fromkeys(removed))

        return cleaned, list(dict.fromkeys(removed))

    def match_redirect(self, query: str, rules: list[dict[str, Any]]) -> RedirectMatch | None:
        query_used = "" if query is None else str(query).strip()
        query_norm = self._normalize_text(query_used)
        if query_norm == "" or not rules:
            return None

        for rule in rules:
            match_type = str(rule.get("match", "contains"))
            url = str(rule.get("url", "")).strip()
            priority = int(rule.get("priority", 0))
            phrases = rule.get("phrases", [])

            if url == "" or not isinstance(phrases, list):
                continue

            for phrase in phrases:
                phrase_norm = self._normalize_text(str(phrase))
                if phrase_norm == "":
                    continue

                is_match = False
                if match_type == "equals":
                    is_match = query_norm == phrase_norm
                elif match_type == "regex":
                    try:
                        is_match = re.search(phrase_norm, query_norm) is not None
                    except re.error:
                        is_match = False
                else:
                    is_match = phrase_norm in query_norm

                if is_match:
                    return RedirectMatch(
                        url=url,
                        match_type=match_type,
                        priority=priority,
                        matched_phrase=phrase_norm,
                        query_used=query_used,
                    )

        return None

    def resolve(
        self,
        query: str,
        platform: str,
        tenant_id: str,
        locale: str,
        store_code: str,
    ) -> dict[str, Any]:
        config = self._load_scoped_config(
            platform=platform,
            tenant_id=tenant_id,
            locale=locale,
            store_code=store_code,
        )

        stopwords = self._extract_stopwords(config)
        redirects = self._extract_redirects(config)
        cleaned_query, removed_stopwords = self.apply_stopwords(query=query, stopwords=stopwords)

        redirect_match = self.match_redirect(query=query, rules=redirects)
        if redirect_match is None and cleaned_query != str(query).strip():
            redirect_match = self.match_redirect(query=cleaned_query, rules=redirects)

        return {
            "query_after_stopwords": cleaned_query,
            "removed_stopwords": removed_stopwords,
            "redirect_match": redirect_match.to_dict() if redirect_match else None,
        }
