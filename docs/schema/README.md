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