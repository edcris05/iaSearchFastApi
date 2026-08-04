# Node Description Batch 1 of 7

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
LANGUAGE: each entry has a `lang=` marker giving the language of its source.
Write that entry's description in EXACTLY that language. Do not translate to
a single common language — match each node's source language individually.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "branch:repo:github.com/edcris05/iaSearchFastApi#main": "main" | kind=Branch | source=git | neighbors=[050dc6f feat: generic scope/domain prof…, 1a1a6aa add logs, 26dec16 fix to get correct credencials, 324741e fix: problems with chat voice, 3786eb2 fix: safe prompt rendering with…, 3b16823 Fallback to legacy default embe…] | lang=en
- "commit:repo:github.com/edcris05/iaSearchFastApi@a7c7838a3f1ec9131ff49a0f885814cf28ed324e": "a7c7838 Initial commit: FastAPI AI search backend docs and source" | kind=Commit | source=git | neighbors=[main, 5d6519d Enforce active correction uniqu…, __init__.py, embedded_phrase.sql, contracts.py, corrections.py] | lang=en
- "models_contracts": "contracts.py" | kind=code-symbol | source=src/models/contracts.py:L1 | neighbors=[050dc6f feat: generic scope/domain prof…, 7be5620 feat: add top-k retrieval diagn…, 92f7548 adding redirects and stopwords, 9787108 add rerank, a7c7838 Initial commit: FastAPI AI sear…, b599c82 add chat turns] | lang=en
- "routers_chat_turn": "chat_turn.py" | kind=code-symbol | source=src/routers/chat_turn.py:L1 | neighbors=[050dc6f feat: generic scope/domain prof…, 1a1a6aa add logs, 324741e fix: problems with chat voice, b599c82 add chat turns, _build_explanation(), _build_search_text()] | lang=en
- "models_contracts_strictbasemodel": "StrictBaseModel" | kind=code-symbol | source=src/models/contracts.py:L12 | neighbors=[contracts.py, AppliedCorrectionOut, ChatContextOut, ChatTurnIn, ChatTurnOut, CorrectionCreate] | lang=en
- "models_embedded_phrase_embeddedphrase": "EmbeddedPhrase" | kind=code-symbol | source=src/models/embedded_phrase.py:L16 | neighbors=[embedded_phrase.py, GenericPostgresql, ._extract_client_suffix(), .__init__(), .insert_row(), ._load_attr_min_margin()] | lang=en
- "routers_user_queries": "user_queries.py" | kind=code-symbol | source=src/routers/user_queries.py:L1 | neighbors=[050dc6f feat: generic scope/domain prof…, 7be5620 feat: add top-k retrieval diagn…, 8e8d84e Scope embedded phrases by tenan…, 92f7548 adding redirects and stopwords, a7c7838 Initial commit: FastAPI AI sear…, b5ddc30 fixes when we use the phrases i…] | lang=en
- "commit:repo:github.com/edcris05/iaSearchFastApi@050dc6febb9bcc923921dfe7dd06fa8906f4f8bc": "050dc6f feat: generic scope/domain profile for intent extraction + scope contra…" | kind=Commit | source=git | neighbors=[main, dc0aeeb add graphify to gitignore, contracts.py, corrections.py, embedded_phrase.py, embedded_phrase_base.py] | lang=en
- "models_generic_postgresql_genericpostgresql": "GenericPostgresql" | kind=code-symbol | source=src/models/generic_postgresql.py:L24 | neighbors=[ChatSessionContextRepository, AppliedCorrection, CorrectionsRepository, DuplicateActiveCorrectionError, EmbeddedPhrase, # TODO: this function may change, and u…] | lang=en
- "text_generation_v2": "v2.py" | kind=code-symbol | source=src/response_api/text_generation/v2.py:L1 | neighbors=[050dc6f feat: generic scope/domain prof…, 3786eb2 fix: safe prompt rendering with…, 4aa3dd2 fix ssl problem v3, 5417f49 fix after updates of generic st…, 7be5620 feat: add top-k retrieval diagn…, 8e8d84e Scope embedded phrases by tenan…] | lang=en
- "models_embedded_phrase": "embedded_phrase.py" | kind=code-symbol | source=src/models/embedded_phrase.py:L1 | neighbors=[050dc6f feat: generic scope/domain prof…, 3b16823 Fallback to legacy default embe…, 5d1fb21 add rerank config, 7be5620 feat: add top-k retrieval diagn…, 7c5f9ce fixes for typo, 8e8d84e Scope embedded phrases by tenan…] | lang=en
- "scripts_eval_topk": "eval_topk.py" | kind=code-symbol | source=scripts/eval_topk.py:L1 | neighbors=[ac8404a changes after test re rank, aggregate(), _as_number_or_none(), build_call_url(), compare_to_baseline(), EvalRow] | lang=en
- "models_corrections_correctionsrepository": "CorrectionsRepository" | kind=code-symbol | source=src/models/corrections.py:L31 | neighbors=[corrections.py, GenericPostgresql, .apply_corrections(), .create_correction(), .deactivate_correction(), ._find_active_duplicate_id()] | lang=en
- "models_query_rules_queryrulesresolver": "QueryRulesResolver" | kind=code-symbol | source=src/models/query_rules.py:L27 | neighbors=[query_rules.py, .apply_stopwords(), ._extract_redirects(), ._extract_stopwords(), ._load_scoped_config(), .match_redirect()] | lang=en
- "routers_chat_turn_handle_chat_turn": "_handle_chat_turn()" | kind=code-symbol | source=src/routers/chat_turn.py:L292 | neighbors=[chat_turn.py, chat_turn(), chat_turn_no_trailing_slash(), _build_explanation(), _build_search_text(), _detect_intent()] | lang=en
- "text_generation_v2_generatorv2": "GeneratorV2" | kind=code-symbol | source=src/response_api/text_generation/v2.py:L30 | neighbors=[v2.py, EmbeddedPhrase, OpenAIEmbedder, .clear_model_response(), ._default_prompt_template(), .extract_search_intent()] | lang=en
- "commit:repo:github.com/edcris05/iaSearchFastApi@8e8d84eafe2e2195476d004e4aebd63cf80c60e2": "8e8d84e Scope embedded phrases by tenant and store" | kind=Commit | source=git | neighbors=[5d6519d Enforce active correction uniqu…, main, 3b16823 Fallback to legacy default embe…, embedded_phrase.py, embedded_phrase_base.py, text_uploaders.py] | lang=en
- "scripts_eval_topk_main": "main()" | kind=code-symbol | source=scripts/eval_topk.py:L318 | neighbors=[eval_topk.py, aggregate(), build_call_url(), compare_to_baseline(), fetch_json(), load_queries()] | lang=en
- "commit:repo:github.com/edcris05/iaSearchFastApi@ffd8c5fcca25e4401ec81251f139618d1b6d7572": "ffd8c5f Protect admin endpoints and formalize v1 response contract" | kind=Commit | source=git | neighbors=[c38131e Document embedded phrase scope …, main, 7be5620 feat: add top-k retrieval diagn…, contracts.py, corrections.py, metrics.py] | lang=en
- "models_embedded_phrase_embeddedphrase_select_row_for_scope": "._select_row_for_scope()" | kind=code-symbol | source=src/models/embedded_phrase.py:L129 | neighbors=[EmbeddedPhrase, ._extract_client_suffix(), ._load_attr_min_margin(), ._load_attr_min_similarity_delta(), ._load_rerank_config(), ._normalize_phrase_text()] | lang=en
- "routers_corrections": "corrections.py" | kind=code-symbol | source=src/routers/corrections.py:L1 | neighbors=[050dc6f feat: generic scope/domain prof…, 5d6519d Enforce active correction uniqu…, a7c7838 Initial commit: FastAPI AI sear…, ffd8c5f Protect admin endpoints and for…, create_correction(), delete_correction()] | lang=en
- "commit:repo:github.com/edcris05/iaSearchFastApi@7be5620690389ff0dc6ed916f1be12650612dcc9": "7be5620 feat: add top-k retrieval diagnostics and configurable attribute thresh…" | kind=Commit | source=git | neighbors=[main, cda8c70 fixes v1, contracts.py, embedded_phrase.py, user_queries.py, v2.py] | lang=en
- "commit:repo:github.com/edcris05/iaSearchFastApi@b599c8277996445b0a93729dbb108996ddc036fe": "b599c82 add chat turns" | kind=Commit | source=git | neighbors=[8ac887c update graphify, main, 1a1a6aa add logs, chat_session_context.py, contracts.py, chat_turn.py] | lang=en
- "commit:repo:github.com/edcris05/iaSearchFastApi@e630bec6984f4cbdc23efd47f613c72ab4043f3f": "e630bec fix to get correct credencials v3" | kind=Commit | source=git | neighbors=[97b6afa fix to get correct credencials …, main, 5d1fb21 add rerank config, generic_postgresql.py, connector.py, user_queries.py] | lang=en
- "models_chat_session_context_chatsessioncontextrepository": "ChatSessionContextRepository" | kind=code-symbol | source=src/models/chat_session_context.py:L7 | neighbors=[chat_session_context.py, GenericPostgresql, .ensure_table(), .load_context(), .reset_context(), .save_context()] | lang=en
- "models_generic_postgresql": "generic_postgresql.py" | kind=code-symbol | source=src/models/generic_postgresql.py:L1 | neighbors=[26dec16 fix to get correct credencials, 97b6afa fix to get correct credencials …, a7c7838 Initial commit: FastAPI AI sear…, e630bec fix to get correct credencials …, _env(), GenericPostgresql] | lang=en
- "models_query_rules_queryrulesresolver_resolve": ".resolve()" | kind=code-symbol | source=src/models/query_rules.py:L236 | neighbors=[QueryRulesResolver, .apply_stopwords(), ._extract_redirects(), ._extract_stopwords(), ._load_scoped_config(), .match_redirect()] | lang=en
- "models_search_event_searcheventrepository": "SearchEventRepository" | kind=code-symbol | source=src/models/search_event.py:L10 | neighbors=[search_event.py, GenericPostgresql, GenericPostgresql, ._build_where(), .export_events_csv(), .export_metrics_summary()] | lang=en
- "postgresql_connector": "connector.py" | kind=code-symbol | source=src/dbpersistence/postgresql/connector.py:L1 | neighbors=[26dec16 fix to get correct credencials, 97b6afa fix to get correct credencials …, a7c7838 Initial commit: FastAPI AI sear…, e630bec fix to get correct credencials …, _env(), _load_project_env()] | lang=en
- "commit:repo:github.com/edcris05/iaSearchFastApi@5d6519d08f80365ec971b6e20cc5def09e23ea7d": "5d6519d Enforce active correction uniqueness in API and DB docs" | kind=Commit | source=git | neighbors=[main, 8e8d84e Scope embedded phrases by tenan…, corrections.py, corrections.py, 001_corrections_active_uniqueness.sql, a7c7838 Initial commit: FastAPI AI sear…] | lang=en
- "commit:repo:github.com/edcris05/iaSearchFastApi@92f75484fa40371acdcac115ac9bda7c8f52670f": "92f7548 adding redirects and stopwords" | kind=Commit | source=git | neighbors=[main, b5ddc30 fixes when we use the phrases i…, contracts.py, query_rules.py, user_queries.py, d3311b3 add graphify] | lang=en
- "commit:repo:github.com/edcris05/iaSearchFastApi@b5ddc30322d59d47782c286d00dc807b1b9b3fac": "b5ddc30 fixes when we use the phrases import" | kind=Commit | source=git | neighbors=[92f7548 adding redirects and stopwords, main, 7c5f9ce fixes for typo, embedded_phrase.py, user_queries.py, v2.py] | lang=en
- "models_corrections": "corrections.py" | kind=code-symbol | source=src/models/corrections.py:L1 | neighbors=[050dc6f feat: generic scope/domain prof…, 5d6519d Enforce active correction uniqu…, a7c7838 Initial commit: FastAPI AI sear…, AppliedCorrection, CorrectionsRepository, DuplicateActiveCorrectionError] | lang=en
- "models_corrections_duplicateactivecorrectionerror": "DuplicateActiveCorrectionError" | kind=code-symbol | source=src/models/corrections.py:L25 | neighbors=[corrections.py, .create_correction(), .update_correction(), Exception, .__init__(), GenericPostgresql] | lang=en
- "postgresql_connector_postgresqlconnector": "PostgreSqlConnector" | kind=code-symbol | source=src/dbpersistence/postgresql/connector.py:L25 | neighbors=[GenericPostgresql, connector.py, .close_connection(), .get_connection(), .__init__(), .insert_single_row()] | lang=en
- "routers_metrics": "metrics.py" | kind=code-symbol | source=src/routers/metrics.py:L1 | neighbors=[a7c7838 Initial commit: FastAPI AI sear…, ffd8c5f Protect admin endpoints and for…, export_csv(), log_event(), _parse_iso_dt(), summary()] | lang=en
- "routers_user_queries_get_response": "get_response()" | kind=code-symbol | source=src/routers/user_queries.py:L142 | neighbors=[user_queries.py, _empty_retrieval(), _load_attribute_min_similarity(), _normalize_filters(), _to_int(), _normalize_response_block()] | lang=en
- "tests_test_domain_profile_contract_domainprofilecontracttests": "DomainProfileContractTests" | kind=code-symbol | source=tests/test_domain_profile_contract.py:L8 | neighbors=[test_domain_profile_contract.py, .setUp(), .tearDown(), .test_domain_profile_scoped_override(), .test_normalize_domain_profile_fallback…, .test_normalize_response_uses_aliases_a…] | lang=en
- "text_generation_v2_generatorv2_extract_search_intent": ".extract_search_intent()" | kind=code-symbol | source=src/response_api/text_generation/v2.py:L162 | neighbors=[GeneratorV2, _debug_enabled(), .clear_model_response(), ._render_prompt(), ._resolve_prompt_template(), ._resolve_system_prompt()] | lang=en
- "commit:repo:github.com/edcris05/iaSearchFastApi@1a1a6aacaf81a221c0c1d56043ec5c1ea64b4b0c": "1a1a6aa add logs" | kind=Commit | source=git | neighbors=[main, 050dc6f feat: generic scope/domain prof…, chat_turn.py, main.py, b599c82 add chat turns] | lang=pt

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
