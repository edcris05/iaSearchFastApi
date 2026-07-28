# Node Description Batch 4 of 5

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
For an entity node (any other kind — e.g. a person, place, event, object),
describe what the entity is and its role, grounded in its type, its
relations (neighbors) and the provided citations/evidence — e.g.
"Lady Carfax, a wealthy heiress who disappears en route to Lausanne.".
Ground entity descriptions in the citations/evidence when present; do not
speculate beyond the context, so a node with no supporting context may be
left out of the reply.
Write every description in Spanish (es). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "routers_metrics_summary": "summary()" | kind=code-symbol | source=src/routers/metrics.py:L29 | neighbors=[metrics.py, _parse_iso_dt()]
- "routers_user_queries_empty_retrieval": "_empty_retrieval()" | kind=code-symbol | source=src/routers/user_queries.py:L103 | neighbors=[user_queries.py, get_response()]
- "routers_user_queries_load_attribute_min_similarity": "_load_attribute_min_similarity()" | kind=code-symbol | source=src/routers/user_queries.py:L112 | neighbors=[user_queries.py, get_response()]
- "routers_user_queries_to_int": "_to_int()" | kind=code-symbol | source=src/routers/user_queries.py:L96 | neighbors=[user_queries.py, get_response()]
- "scripts_eval_topk_as_number_or_none": "_as_number_or_none()" | kind=code-symbol | source=scripts/eval_topk.py:L63 | neighbors=[eval_topk.py, parse_eval_row()]
- "scripts_eval_topk_build_call_url": "build_call_url()" | kind=code-symbol | source=scripts/eval_topk.py:L163 | neighbors=[eval_topk.py, main()]
- "scripts_eval_topk_compare_to_baseline": "compare_to_baseline()" | kind=code-symbol | source=scripts/eval_topk.py:L227 | neighbors=[eval_topk.py, main()]
- "scripts_eval_topk_evalrow": "EvalRow" | kind=code-symbol | source=scripts/eval_topk.py:L28 | neighbors=[eval_topk.py, parse_eval_row()]
- "scripts_eval_topk_fetch_json": "fetch_json()" | kind=code-symbol | source=scripts/eval_topk.py:L92 | neighbors=[eval_topk.py, main()]
- "scripts_eval_topk_load_queries": "load_queries()" | kind=code-symbol | source=scripts/eval_topk.py:L77 | neighbors=[eval_topk.py, main()]
- "scripts_eval_topk_parse_args": "parse_args()" | kind=code-symbol | source=scripts/eval_topk.py:L46 | neighbors=[eval_topk.py, main()]
- "scripts_eval_topk_percentile": "percentile()" | kind=code-symbol | source=scripts/eval_topk.py:L214 | neighbors=[eval_topk.py, aggregate()]
- "scripts_eval_topk_write_raw_csv": "write_raw_csv()" | kind=code-symbol | source=scripts/eval_topk.py:L277 | neighbors=[eval_topk.py, main()]
- "src_main": "main.py" | kind=code-symbol | source=src/main.py:L1 | neighbors=[a7c7838 Initial commit: FastAPI AI sear…, home()]
- "text_generation_v1": "v1.py" | kind=code-symbol | source=src/response_api/text_generation/v1.py:L1 | neighbors=[a7c7838 Initial commit: FastAPI AI sear…, V1]
- "text_generation_v2_generatorv2_clear_model_response": ".clear_model_response()" | kind=code-symbol | source=src/response_api/text_generation/v2.py:L140 | neighbors=[GeneratorV2, .extract_search_intent()]
- "text_generation_v2_generatorv2_get_embedding_filter_by_attributes": ".get_embedding_filter_by_attributes()" | kind=code-symbol | source=src/response_api/text_generation/v2.py:L145 | neighbors=[GeneratorV2, _debug_enabled()]
- "utils_auth": "auth.py" | kind=code-symbol | source=src/utils/auth.py:L1 | neighbors=[ffd8c5f Protect admin endpoints and for…, require_admin_api_key()]
- "utils_config": "config.py" | kind=code-symbol | source=src/utils/config.py:L1 | neighbors=[a7c7838 Initial commit: FastAPI AI sear…, get_openai_key()]
- "dbpersistence_init": "__init__.py" | kind=code-symbol | source=src/dbpersistence/__init__.py:L1 | neighbors=[a7c7838 Initial commit: FastAPI AI sear…]
- "embedded_phrase_public_embedded_phrase": "public.embedded_phrase" | kind=code-symbol | source=embedded_phrase.sql:L29 | neighbors=[embedded_phrase.sql]
- "exception": "Exception" | kind=code-symbol | neighbors=[DuplicateActiveCorrectionError]
- "models_corrections_duplicateactivecorrectionerror_init": ".__init__()" | kind=code-symbol | source=src/models/corrections.py:L25 | neighbors=[DuplicateActiveCorrectionError]
- "models_embedded_phrase_embeddedphrase_init": ".__init__()" | kind=code-symbol | source=src/models/embedded_phrase.py:L30 | neighbors=[EmbeddedPhrase]
- "models_embedded_phrase_embeddedphrase_insert_row": ".insert_row()" | kind=code-symbol | source=src/models/embedded_phrase.py:L55 | neighbors=[EmbeddedPhrase]
- "models_generic_postgresql_load_project_env": "_load_project_env()" | kind=code-symbol | source=src/models/generic_postgresql.py:L8 | neighbors=[generic_postgresql.py]
- "models_init": "__init__.py" | kind=code-symbol | source=src/models/__init__.py:L1 | neighbors=[a7c7838 Initial commit: FastAPI AI sear…]
- "models_query_rules_rationale_28": "Resuelve stopwords y redirects por scope multi-commerce.      Env vars soportada" | kind=entity | source=src/models/query_rules.py:L28 | neighbors=[QueryRulesResolver]
- "models_search_event_searcheventrepository_log_event": ".log_event()" | kind=code-symbol | source=src/models/search_event.py:L11 | neighbors=[SearchEventRepository]
- "postgresql_connector_load_project_env": "_load_project_env()" | kind=code-symbol | source=src/dbpersistence/postgresql/connector.py:L8 | neighbors=[connector.py]
- "postgresql_connector_postgresqlconnector_close_connection": ".close_connection()" | kind=code-symbol | source=src/dbpersistence/postgresql/connector.py:L50 | neighbors=[PostgreSqlConnector]
- "postgresql_init": "__init__.py" | kind=code-symbol | source=src/dbpersistence/postgresql/__init__.py:L1 | neighbors=[a7c7838 Initial commit: FastAPI AI sear…]
- "response_api_init": "__init__.py" | kind=code-symbol | source=src/response_api/__init__.py:L1 | neighbors=[a7c7838 Initial commit: FastAPI AI sear…]
- "response_api_openai_embedder_openaiembedder_get_embedding": ".get_embedding()" | kind=code-symbol | source=src/response_api/openai_embedder.py:L39 | neighbors=[OpenAIEmbedder]
- "response_api_openai_embedder_openaiembedder_init": ".__init__()" | kind=code-symbol | source=src/response_api/openai_embedder.py:L26 | neighbors=[OpenAIEmbedder]
- "response_api_openai_embedder_openaiembedder_repr": ".__repr__()" | kind=code-symbol | source=src/response_api/openai_embedder.py:L56 | neighbors=[OpenAIEmbedder]
- "routers_corrections_create_correction": "create_correction()" | kind=code-symbol | source=src/routers/corrections.py:L30 | neighbors=[corrections.py]
- "routers_corrections_delete_correction": "delete_correction()" | kind=code-symbol | source=src/routers/corrections.py:L66 | neighbors=[corrections.py]
- "routers_corrections_list_corrections": "list_corrections()" | kind=code-symbol | source=src/routers/corrections.py:L12 | neighbors=[corrections.py]
- "routers_corrections_update_correction": "update_correction()" | kind=code-symbol | source=src/routers/corrections.py:L46 | neighbors=[corrections.py]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /home/edgar/projects/pythonProjects/fastApi1/.graphify/description-instructions/batch-003.json

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
