# API Schemas

- [get_response_v1.schema.json](get_response_v1.schema.json)

Notes:
- This schema documents the strict `GET /get_response/v1` contract implemented in FastAPI.
- It is versioned as a standalone artifact so consumers can validate payloads independently of runtime code.

Retrieval tuning:
- Global threshold is controlled by query param `min_similarity`.
- Per-attribute threshold override is controlled by env var `EMBEDDING_MIN_SIMILARITY_BY_ATTRIBUTE` as JSON.
- Example: `{\"color\":0.5,\"movistar_screentechnology\":0.42}`.
- Keep tenant/provider-specific attribute codes out of source defaults; define them per environment.

Rerank tuning (retrieval):
- `RETRIEVAL_RERANK_VERSION` (default: `rerank_v1`).
- `RETRIEVAL_RERANK_WEIGHTS` as JSON (default semantic/margin/business = `0.80/0.10/0.10`).
- `RETRIEVAL_BUSINESS_BOOSTS` as JSON map.
- Boost key formats supported:
	- `attribute_code::attribute_value_number` (e.g. `color::133`)
	- `attribute_code::attribute_value_string` (e.g. `brand::samsung`)
	- `phrase::phrase text`
	- `attr::attribute_code`
- Scoped overrides are supported per deployment scope:
	- `RETRIEVAL_RERANK_VERSION__<PLATFORM>__<TENANT>__<LOCALE>__<STORE>`
	- `RETRIEVAL_RERANK_WEIGHTS__<PLATFORM>__<TENANT>__<LOCALE>__<STORE>`
	- `RETRIEVAL_BUSINESS_BOOSTS__<PLATFORM>__<TENANT>__<LOCALE>__<STORE>`
	- Broad to specific fallback is applied: `PLATFORM` -> `PLATFORM+TENANT` -> `PLATFORM+TENANT+LOCALE` -> full scope.
	- Example: `RETRIEVAL_RERANK_WEIGHTS__MAGENTO__BASE__ES_AR__DEFAULT={"semantic":0.82,"margin":0.08,"business":0.10}`

Query rules (stopwords + redirects):
- `QUERY_RULES_JSON` as JSON with optional keys: `stopwords`, `redirects`.
- Scoped overrides are supported with the same pattern:
	- `QUERY_RULES_JSON__<PLATFORM>__<TENANT>__<LOCALE>__<STORE>`
- Redirect rule format:
	- `{"phrases":["linea nueva"],"match":"contains","url":"https://...","priority":3}`
- Supported `match`: `contains`, `equals`, `regex`.
- Response meta now includes:
	- `redirect_url`, `redirect_match`, `query_after_stopwords`, `removed_stopwords`.

Operational runbook (multi-clone env hygiene):
- Keep real secrets only in local `.env` files, never in git-tracked files.
- Use `.env.example` as the canonical template and copy it per runtime clone.
- For each clone (for example `/home/edgar/...` and `/home/magento/...`), run:
	1. `cp .env.example .env` (first time only)
	2. Set real values for `OPENAI_API_KEY` and DB credentials.
	3. Keep rerank defaults identical unless intentionally testing scope variants.
- After rotating keys, update both clones in the same maintenance window.
- Validate startup before traffic:
	- DB connector initializes without auth errors.
	- `GET /get_response/v1` returns `source=semantic` for a known semantic query.
- If one clone degrades to fallback while the other is healthy, first compare `.env` values between clones.