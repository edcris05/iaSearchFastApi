# Node Description Batch 1 of 5

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
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "commit:repo:github.com/edcris05/iaSearchFastApi@a7c7838a3f1ec9131ff49a0f885814cf28ed324e": "a7c7838 Initial commit: FastAPI AI search backend docs and source" | kind=Commit | source=git | neighbors=[main, 5d6519d Enforce active correction uniqu…, __init__.py, embedded_phrase.sql, contracts.py, corrections.py]
- "branch:repo:github.com/edcris05/iaSearchFastApi#main": "main" | kind=Branch | source=git | neighbors=[26dec16 fix to get correct credencials, 3b16823 Fallback to legacy default embe…, 5d1fb21 add rerank config, 5d6519d Enforce active correction uniqu…, 7be5620 feat: add top-k retrieval diagn…, 7c5f9ce fixes for typo]
- "models_contracts": "contracts.py" | kind=code-symbol | source=src/models/contracts.py:L1 | neighbors=[7be5620 feat: add top-k retrieval diagn…, 92f7548 adding redirects and stopwords, 9787108 add rerank, a7c7838 Initial commit: FastAPI AI sear…, ffd8c5f Protect admin endpoints and for…, AppliedCorrectionOut]
- "routers_user_queries": "user_queries.py" | kind=code-symbol | source=src/routers/user_queries.py:L1 | neighbors=[7be5620 feat: add top-k retrieval diagn…, 8e8d84e Scope embedded phrases by tenan…, 92f7548 adding redirects and stopwords, a7c7838 Initial commit: FastAPI AI sear…, b5ddc30 fixes when we use the phrases i…, cda8c70 fixes v1]
- "models_contracts_strictbasemodel": "StrictBaseModel" | kind=code-symbol | source=src/models/contracts.py:L5 | neighbors=[contracts.py, AppliedCorrectionOut, CorrectionCreate, CorrectionUpdate, RetrievalAttributeOut, RetrievalCandidateOut]
- "models_embedded_phrase_embeddedphrase": "EmbeddedPhrase" | kind=code-symbol | source=src/models/embedded_phrase.py:L10 | neighbors=[embedded_phrase.py, GenericPostgresql, ._extract_client_suffix(), .__init__(), .insert_row(), ._load_rerank_config()]
- "scripts_eval_topk": "eval_topk.py" | kind=code-symbol | source=scripts/eval_topk.py:L1 | neighbors=[ac8404a changes after test re rank, aggregate(), _as_number_or_none(), build_call_url(), compare_to_baseline(), EvalRow]
- "models_corrections_correctionsrepository": "CorrectionsRepository" | kind=code-symbol | source=src/models/corrections.py:L30 | neighbors=[corrections.py, GenericPostgresql, .apply_corrections(), .create_correction(), .deactivate_correction(), ._find_active_duplicate_id()]
- "models_generic_postgresql_genericpostgresql": "GenericPostgresql" | kind=code-symbol | source=src/models/generic_postgresql.py:L24 | neighbors=[AppliedCorrection, CorrectionsRepository, DuplicateActiveCorrectionError, EmbeddedPhrase, # TODO: this function may change, and u…, generic_postgresql.py]
- "models_embedded_phrase": "embedded_phrase.py" | kind=code-symbol | source=src/models/embedded_phrase.py:L1 | neighbors=[3b16823 Fallback to legacy default embe…, 5d1fb21 add rerank config, 7be5620 feat: add top-k retrieval diagn…, 7c5f9ce fixes for typo, 8e8d84e Scope embedded phrases by tenan…, 9787108 add rerank]
- "models_query_rules_queryrulesresolver": "QueryRulesResolver" | kind=code-symbol | source=src/models/query_rules.py:L27 | neighbors=[query_rules.py, .apply_stopwords(), ._extract_redirects(), ._extract_stopwords(), ._load_scoped_config(), .match_redirect()]
- "commit:repo:github.com/edcris05/iaSearchFastApi@8e8d84eafe2e2195476d004e4aebd63cf80c60e2": "8e8d84e Scope embedded phrases by tenant and store" | kind=Commit | source=git | neighbors=[5d6519d Enforce active correction uniqu…, main, 3b16823 Fallback to legacy default embe…, embedded_phrase.py, embedded_phrase_base.py, text_uploaders.py]
- "scripts_eval_topk_main": "main()" | kind=code-symbol | source=scripts/eval_topk.py:L318 | neighbors=[eval_topk.py, aggregate(), build_call_url(), compare_to_baseline(), fetch_json(), load_queries()]
- "commit:repo:github.com/edcris05/iaSearchFastApi@ffd8c5fcca25e4401ec81251f139618d1b6d7572": "ffd8c5f Protect admin endpoints and formalize v1 response contract" | kind=Commit | source=git | neighbors=[c38131e Document embedded phrase scope …, main, 7be5620 feat: add top-k retrieval diagn…, contracts.py, corrections.py, metrics.py]
- "text_generation_v2": "v2.py" | kind=code-symbol | source=src/response_api/text_generation/v2.py:L1 | neighbors=[7be5620 feat: add top-k retrieval diagn…, 8e8d84e Scope embedded phrases by tenan…, a7c7838 Initial commit: FastAPI AI sear…, b5ddc30 fixes when we use the phrases i…, d46099c add log to trace, e630bec fix to get correct credencials …]
- "commit:repo:github.com/edcris05/iaSearchFastApi@7be5620690389ff0dc6ed916f1be12650612dcc9": "7be5620 feat: add top-k retrieval diagnostics and configurable attribute thresh…" | kind=Commit | source=git | neighbors=[main, cda8c70 fixes v1, contracts.py, embedded_phrase.py, user_queries.py, v2.py]
- "commit:repo:github.com/edcris05/iaSearchFastApi@e630bec6984f4cbdc23efd47f613c72ab4043f3f": "e630bec fix to get correct credencials v3" | kind=Commit | source=git | neighbors=[97b6afa fix to get correct credencials …, main, 5d1fb21 add rerank config, generic_postgresql.py, connector.py, user_queries.py]
- "models_generic_postgresql": "generic_postgresql.py" | kind=code-symbol | source=src/models/generic_postgresql.py:L1 | neighbors=[26dec16 fix to get correct credencials, 97b6afa fix to get correct credencials …, a7c7838 Initial commit: FastAPI AI sear…, e630bec fix to get correct credencials …, _env(), GenericPostgresql]
- "models_query_rules_queryrulesresolver_resolve": ".resolve()" | kind=code-symbol | source=src/models/query_rules.py:L236 | neighbors=[QueryRulesResolver, .apply_stopwords(), ._extract_redirects(), ._extract_stopwords(), ._load_scoped_config(), .match_redirect()]
- "models_search_event_searcheventrepository": "SearchEventRepository" | kind=code-symbol | source=src/models/search_event.py:L10 | neighbors=[search_event.py, GenericPostgresql, GenericPostgresql, ._build_where(), .export_events_csv(), .export_metrics_summary()]
- "postgresql_connector": "connector.py" | kind=code-symbol | source=src/dbpersistence/postgresql/connector.py:L1 | neighbors=[26dec16 fix to get correct credencials, 97b6afa fix to get correct credencials …, a7c7838 Initial commit: FastAPI AI sear…, e630bec fix to get correct credencials …, _env(), _load_project_env()]
- "routers_corrections": "corrections.py" | kind=code-symbol | source=src/routers/corrections.py:L1 | neighbors=[5d6519d Enforce active correction uniqu…, a7c7838 Initial commit: FastAPI AI sear…, ffd8c5f Protect admin endpoints and for…, create_correction(), delete_correction(), list_corrections()]
- "text_generation_v2_generatorv2": "GeneratorV2" | kind=code-symbol | source=src/response_api/text_generation/v2.py:L21 | neighbors=[v2.py, EmbeddedPhrase, OpenAIEmbedder, .clear_model_response(), .extract_search_intent(), .get_embedding_filter_by_attributes()]
- "commit:repo:github.com/edcris05/iaSearchFastApi@5d6519d08f80365ec971b6e20cc5def09e23ea7d": "5d6519d Enforce active correction uniqueness in API and DB docs" | kind=Commit | source=git | neighbors=[main, 8e8d84e Scope embedded phrases by tenan…, corrections.py, corrections.py, 001_corrections_active_uniqueness.sql, a7c7838 Initial commit: FastAPI AI sear…]
- "commit:repo:github.com/edcris05/iaSearchFastApi@92f75484fa40371acdcac115ac9bda7c8f52670f": "92f7548 adding redirects and stopwords" | kind=Commit | source=git | neighbors=[main, b5ddc30 fixes when we use the phrases i…, contracts.py, query_rules.py, user_queries.py, d3311b3 add graphify]
- "commit:repo:github.com/edcris05/iaSearchFastApi@b5ddc30322d59d47782c286d00dc807b1b9b3fac": "b5ddc30 fixes when we use the phrases import" | kind=Commit | source=git | neighbors=[92f7548 adding redirects and stopwords, main, 7c5f9ce fixes for typo, embedded_phrase.py, user_queries.py, v2.py]
- "models_corrections_duplicateactivecorrectionerror": "DuplicateActiveCorrectionError" | kind=code-symbol | source=src/models/corrections.py:L24 | neighbors=[corrections.py, .create_correction(), .update_correction(), Exception, .__init__(), GenericPostgresql]
- "models_embedded_phrase_embeddedphrase_select_row_for_scope": "._select_row_for_scope()" | kind=code-symbol | source=src/models/embedded_phrase.py:L123 | neighbors=[EmbeddedPhrase, ._extract_client_suffix(), ._load_rerank_config(), ._normalize_phrase_text(), ._resolve_business_boost(), .select_row_with_diagnostics()]
- "postgresql_connector_postgresqlconnector": "PostgreSqlConnector" | kind=code-symbol | source=src/dbpersistence/postgresql/connector.py:L25 | neighbors=[GenericPostgresql, connector.py, .close_connection(), .get_connection(), .__init__(), .insert_single_row()]
- "routers_metrics": "metrics.py" | kind=code-symbol | source=src/routers/metrics.py:L1 | neighbors=[a7c7838 Initial commit: FastAPI AI sear…, ffd8c5f Protect admin endpoints and for…, export_csv(), log_event(), _parse_iso_dt(), summary()]
- "routers_user_queries_get_response": "get_response()" | kind=code-symbol | source=src/routers/user_queries.py:L152 | neighbors=[user_queries.py, _empty_retrieval(), _load_attribute_min_similarity(), _normalize_filters(), _normalize_response_block(), _to_int()]
- "commit:repo:github.com/edcris05/iaSearchFastApi@26dec16627a8dfc5ca12863e3cad9c19f7421338": "26dec16 fix to get correct credencials" | kind=Commit | source=git | neighbors=[main, 97b6afa fix to get correct credencials …, generic_postgresql.py, connector.py, d46099c add log to trace]
- "commit:repo:github.com/edcris05/iaSearchFastApi@97871081e5b876e3a8ff823335083e8500c07393": "9787108 add rerank" | kind=Commit | source=git | neighbors=[main, dc7cc56 add script to swith with severa…, contracts.py, embedded_phrase.py, cda8c70 fixes v1]
- "commit:repo:github.com/edcris05/iaSearchFastApi@97b6afadb51a877a0aec88d3846ce48e2c211271": "97b6afa fix to get correct credencials v2" | kind=Commit | source=git | neighbors=[26dec16 fix to get correct credencials, main, e630bec fix to get correct credencials …, generic_postgresql.py, connector.py]
- "commit:repo:github.com/edcris05/iaSearchFastApi@c38131ed42aa16178483493d342f58a054a3119f": "c38131e Document embedded phrase scope backfill" | kind=Commit | source=git | neighbors=[3b16823 Fallback to legacy default embe…, main, ffd8c5f Protect admin endpoints and for…, embedded_phrase.py, 003_embedded_phrase_backfill_movistar_b…]
- "commit:repo:github.com/edcris05/iaSearchFastApi@d46099c9486d65339ad55e22a284271832bb6de3": "d46099c add log to trace" | kind=Commit | source=git | neighbors=[main, 26dec16 fix to get correct credencials, user_queries.py, v2.py, dc7cc56 add script to swith with severa…]
- "models_corrections": "corrections.py" | kind=code-symbol | source=src/models/corrections.py:L1 | neighbors=[5d6519d Enforce active correction uniqu…, a7c7838 Initial commit: FastAPI AI sear…, AppliedCorrection, CorrectionsRepository, DuplicateActiveCorrectionError]
- "models_corrections_correctionsrepository_update_correction": ".update_correction()" | kind=code-symbol | source=src/models/corrections.py:L237 | neighbors=[CorrectionsRepository, .deactivate_correction(), ._find_active_duplicate_id(), ._write_audit(), DuplicateActiveCorrectionError]
- "models_query_rules_queryrulesresolver_normalize_text": "._normalize_text()" | kind=code-symbol | source=src/models/query_rules.py:L69 | neighbors=[QueryRulesResolver, .apply_stopwords(), ._extract_redirects(), ._extract_stopwords(), .match_redirect()]
- "response_api_openai_embedder_openaiembedder": "OpenAIEmbedder" | kind=code-symbol | source=src/response_api/openai_embedder.py:L25 | neighbors=[openai_embedder.py, .get_embedding(), .__init__(), .__repr__(), GeneratorV2]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /home/edgar/projects/pythonProjects/fastApi1/.graphify/description-instructions/batch-000.json

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
