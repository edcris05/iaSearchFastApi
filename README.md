# fastApi1

## Documentacion

- [AI Search Multi-Commerce](docs/ai-search-multicommerce.md)
- [SQL: Active Correction Uniqueness](docs/sql/001_corrections_active_uniqueness.sql)
- [SQL: Embedded Phrase Multi-Tenant](docs/sql/002_embedded_phrase_multitenant.sql)
- [SQL: Embedded Phrase Backfill Movistar Base](docs/sql/003_embedded_phrase_backfill_movistar_base.sql)
- [API Schemas](docs/schema/README.md)

## Security

- Set `ADMIN_API_KEY` in the FastAPI environment to require the `X-API-Key` header on `/corrections/*` and `/metrics/*`.
- If `ADMIN_API_KEY` is empty or unset, those endpoints remain open for backward-compatible rollout.
