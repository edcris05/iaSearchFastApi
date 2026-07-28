# Node Description Batch 5 of 5

Graphify is running in assistant/skill mode (no API key). You are the host
assistant (Claude Code / Codex / Gemini CLI). Read the prompt below and write
your JSON answer to the answer file.

## Prompt

You are documenting nodes in a knowledge graph.
For each entry below, write ONE concise factual plain-language sentence
describing what it is or does. Use only the provided context.
For a code symbol (kind=code-symbol — a function, class, or constant),
describe what the function/symbol does based on its name, source location
and neighbors — e.g. "Resolves the configured ontology profile from graphify.yaml.".
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "routers_init": "__init__.py" | kind=code-symbol | source=src/routers/__init__.py:L1 | neighbors=[a7c7838 Initial commit: FastAPI AI sear…]
- "routers_metrics_log_event": "log_event()" | kind=code-symbol | source=src/routers/metrics.py:L22 | neighbors=[metrics.py]
- "routers_text_uploaders_copy_2_get_response": "get_response()" | kind=code-symbol | source=src/routers/text_uploaders copy 2.py:L47 | neighbors=[text_uploaders copy 2.py]
- "routers_text_uploaders_copy_2_upload_csv": "upload_csv()" | kind=code-symbol | source=src/routers/text_uploaders copy 2.py:L59 | neighbors=[text_uploaders copy 2.py]
- "routers_text_uploaders_copy_2_upload_phrase": "upload_phrase()" | kind=code-symbol | source=src/routers/text_uploaders copy 2.py:L15 | neighbors=[text_uploaders copy 2.py]
- "routers_text_uploaders_copy_get_response": "get_response()" | kind=code-symbol | source=src/routers/text_uploaders copy.py:L45 | neighbors=[text_uploaders copy.py]
- "routers_text_uploaders_copy_upload_phrase": "upload_phrase()" | kind=code-symbol | source=src/routers/text_uploaders copy.py:L13 | neighbors=[text_uploaders copy.py]
- "routers_text_uploaders_get_response": "get_response()" | kind=code-symbol | source=src/routers/text_uploaders.py:L57 | neighbors=[text_uploaders.py]
- "routers_text_uploaders_upload_phrase": "upload_phrase()" | kind=code-symbol | source=src/routers/text_uploaders.py:L13 | neighbors=[text_uploaders.py]
- "sql_001_corrections_active_uniqueness": "001_corrections_active_uniqueness.sql" | kind=code-symbol | source=docs/sql/001_corrections_active_uniqueness.sql:L1 | neighbors=[5d6519d Enforce active correction uniqu…]
- "sql_002_embedded_phrase_multitenant": "002_embedded_phrase_multitenant.sql" | kind=code-symbol | source=docs/sql/002_embedded_phrase_multitenant.sql:L1 | neighbors=[8e8d84e Scope embedded phrases by tenan…]
- "sql_003_embedded_phrase_backfill_movistar_base": "003_embedded_phrase_backfill_movistar_base.sql" | kind=code-symbol | source=docs/sql/003_embedded_phrase_backfill_movistar_base.sql:L1 | neighbors=[c38131e Document embedded phrase scope …]
- "src_main_home": "home()" | kind=code-symbol | source=src/main.py:L15 | neighbors=[main.py]
- "text_generation_v1_v1_extract_search_intent": ".extract_search_intent()" | kind=code-symbol | source=src/response_api/text_generation/v1.py:L12 | neighbors=[V1]
- "text_generation_v1_v1_init": ".__init__()" | kind=code-symbol | source=src/response_api/text_generation/v1.py:L9 | neighbors=[V1]
- "text_generation_v2_generatorv2_init": ".__init__()" | kind=code-symbol | source=src/response_api/text_generation/v2.py:L22 | neighbors=[GeneratorV2]
- "utils_auth_require_admin_api_key": "require_admin_api_key()" | kind=code-symbol | source=src/utils/auth.py:L6 | neighbors=[auth.py]
- "utils_config_get_openai_key": "get_openai_key()" | kind=code-symbol | source=src/utils/config.py:L4 | neighbors=[config.py]
- "utils_init": "__init__.py" | kind=code-symbol | source=src/utils/__init__.py:L1 | neighbors=[a7c7838 Initial commit: FastAPI AI sear…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /home/edgar/projects/pythonProjects/fastApi1/.graphify/description-instructions/batch-004.json

Keep each description factual and concise (one sentence). No markdown, no prose
outside the JSON object. It is acceptable to omit a node if context is
insufficient — but include every node you can ground confidently.

Example answer format:
```json
{
  "node_id_1": "Resolves the configured ontology profile from graphify.yaml.",
  "node_id_2": "Colonel James Barclay, an antagonist in The Crooked Man."
}
```
