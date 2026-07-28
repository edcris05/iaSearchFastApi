# Node Description Batch 2 of 5

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

- "commit:repo:github.com/edcris05/iaSearchFastApi@3b1682376b15af3cd66918ae37658c6dfbf73a77": "3b16823 Fallback to legacy default embedding scope" | kind=Commit | source=git | neighbors=[main, c38131e Document embedded phrase scope …, embedded_phrase.py, 8e8d84e Scope embedded phrases by tenan…] | lang=en
- "commit:repo:github.com/edcris05/iaSearchFastApi@5d1fb2112c83697600e126f1858820eaa7f08855": "5d1fb21 add rerank config" | kind=Commit | source=git | neighbors=[main, ac8404a changes after test re rank, embedded_phrase.py, e630bec fix to get correct credencials …] | lang=en
- "commit:repo:github.com/edcris05/iaSearchFastApi@ac8404a18ccec5125ce23ecddf3a6a5ee8d511e5": "ac8404a changes after test re rank" | kind=Commit | source=git | neighbors=[5d1fb21 add rerank config, main, d3311b3 add graphify, eval_topk.py] | lang=pt
- "commit:repo:github.com/edcris05/iaSearchFastApi@cda8c7092d9d22167ab6d00bb9f615af07cf8593": "cda8c70 fixes v1" | kind=Commit | source=git | neighbors=[7be5620 feat: add top-k retrieval diagn…, main, 9787108 add rerank, user_queries.py] | lang=en
- "models_corrections_correctionsrepository_create_correction": ".create_correction()" | kind=code-symbol | source=src/models/corrections.py:L155 | neighbors=[CorrectionsRepository, ._find_active_duplicate_id(), ._write_audit(), DuplicateActiveCorrectionError] | lang=en
- "models_corrections_correctionsrepository_write_audit": "._write_audit()" | kind=code-symbol | source=src/models/corrections.py:L94 | neighbors=[CorrectionsRepository, .create_correction(), .deactivate_correction(), .update_correction()] | lang=en
- "models_query_rules_queryrulesresolver_match_redirect": ".match_redirect()" | kind=code-symbol | source=src/models/query_rules.py:L194 | neighbors=[QueryRulesResolver, ._normalize_text(), RedirectMatch, .resolve()] | lang=en
- "routers_text_uploaders": "text_uploaders.py" | kind=code-symbol | source=src/routers/text_uploaders.py:L1 | neighbors=[8e8d84e Scope embedded phrases by tenan…, a7c7838 Initial commit: FastAPI AI sear…, get_response(), upload_phrase()] | lang=en
- "routers_text_uploaders_copy_2": "text_uploaders copy 2.py" | kind=code-symbol | source=src/routers/text_uploaders copy 2.py:L1 | neighbors=[a7c7838 Initial commit: FastAPI AI sear…, get_response(), upload_csv(), upload_phrase()] | lang=en
- "scripts_eval_topk_parse_eval_row": "parse_eval_row()" | kind=code-symbol | source=scripts/eval_topk.py:L114 | neighbors=[eval_topk.py, main(), _as_number_or_none(), EvalRow] | lang=en
- "commit:repo:github.com/edcris05/iaSearchFastApi@7c5f9cedc985dbef96f3a4b6bf87daf210c604eb": "7c5f9ce fixes for typo" | kind=Commit | source=git | neighbors=[main, embedded_phrase.py, b5ddc30 fixes when we use the phrases i…] | lang=en
- "commit:repo:github.com/edcris05/iaSearchFastApi@d3311b34d04e5b997f56f9263d0c6242ffc2f86a": "d3311b3 add graphify" | kind=Commit | source=git | neighbors=[ac8404a changes after test re rank, main, 92f7548 adding redirects and stopwords] | lang=en
- "commit:repo:github.com/edcris05/iaSearchFastApi@dc7cc5679a5f59cf86ccc0885023da890f64be06": "dc7cc56 add script to swith with several profiles" | kind=Commit | source=git | neighbors=[9787108 add rerank, main, d46099c add log to trace] | lang=en
- "genericpostgresql": "GenericPostgresql" | kind=code-symbol | neighbors=[CorrectionsRepository, EmbeddedPhrase, SearchEventRepository] | lang=en
- "models_corrections_correctionsrepository_apply_corrections": ".apply_corrections()" | kind=code-symbol | source=src/models/corrections.py:L391 | neighbors=[CorrectionsRepository, .list_corrections(), ._matches()] | lang=en
- "models_corrections_correctionsrepository_deactivate_correction": ".deactivate_correction()" | kind=code-symbol | source=src/models/corrections.py:L353 | neighbors=[CorrectionsRepository, .update_correction(), ._write_audit()] | lang=en
- "models_corrections_correctionsrepository_find_active_duplicate_id": "._find_active_duplicate_id()" | kind=code-symbol | source=src/models/corrections.py:L122 | neighbors=[CorrectionsRepository, .create_correction(), .update_correction()] | lang=en
- "models_corrections_correctionsrepository_matches": "._matches()" | kind=code-symbol | source=src/models/corrections.py:L366 | neighbors=[CorrectionsRepository, .apply_corrections(), ._normalize()] | lang=en
- "models_embedded_phrase_base": "embedded_phrase_base.py" | kind=code-symbol | source=src/models/embedded_phrase_base.py:L1 | neighbors=[8e8d84e Scope embedded phrases by tenan…, a7c7838 Initial commit: FastAPI AI sear…, EmbeddedPhraseUploadBase] | lang=en
- "models_embedded_phrase_embeddedphrase_load_rerank_config": "._load_rerank_config()" | kind=code-symbol | source=src/models/embedded_phrase.py:L376 | neighbors=[EmbeddedPhrase, ._scoped_env_names(), ._select_row_for_scope()] | lang=en
- "models_embedded_phrase_embeddedphrase_scoped_env_names": "._scoped_env_names()" | kind=code-symbol | source=src/models/embedded_phrase.py:L355 | neighbors=[EmbeddedPhrase, ._load_rerank_config(), ._scope_part()] | lang=en
- "models_embedded_phrase_embeddedphrase_select_row_with_diagnostics": ".select_row_with_diagnostics()" | kind=code-symbol | source=src/models/embedded_phrase.py:L99 | neighbors=[EmbeddedPhrase, .select_row(), ._select_row_for_scope()] | lang=en
- "models_generic_postgresql_genericpostgresql_get_connection": ".get_connection()" | kind=code-symbol | source=src/models/generic_postgresql.py:L45 | neighbors=[GenericPostgresql, .execute_select(), .insert_single_row()] | lang=en
- "models_query_rules": "query_rules.py" | kind=code-symbol | source=src/models/query_rules.py:L1 | neighbors=[92f7548 adding redirects and stopwords, QueryRulesResolver, RedirectMatch] | lang=en
- "models_query_rules_queryrulesresolver_apply_stopwords": ".apply_stopwords()" | kind=code-symbol | source=src/models/query_rules.py:L168 | neighbors=[QueryRulesResolver, ._normalize_text(), .resolve()] | lang=en
- "models_query_rules_queryrulesresolver_extract_redirects": "._extract_redirects()" | kind=code-symbol | source=src/models/query_rules.py:L120 | neighbors=[QueryRulesResolver, ._normalize_text(), .resolve()] | lang=en
- "models_query_rules_queryrulesresolver_extract_stopwords": "._extract_stopwords()" | kind=code-symbol | source=src/models/query_rules.py:L107 | neighbors=[QueryRulesResolver, ._normalize_text(), .resolve()] | lang=en
- "models_query_rules_queryrulesresolver_load_scoped_config": "._load_scoped_config()" | kind=code-symbol | source=src/models/query_rules.py:L78 | neighbors=[QueryRulesResolver, ._scoped_env_names(), .resolve()] | lang=en
- "models_query_rules_queryrulesresolver_scoped_env_names": "._scoped_env_names()" | kind=code-symbol | source=src/models/query_rules.py:L49 | neighbors=[QueryRulesResolver, ._load_scoped_config(), ._scope_part()] | lang=en
- "models_query_rules_redirectmatch": "RedirectMatch" | kind=code-symbol | source=src/models/query_rules.py:L10 | neighbors=[query_rules.py, .match_redirect(), .to_dict()] | lang=en
- "models_search_event_searcheventrepository_build_where": "._build_where()" | kind=code-symbol | source=src/models/search_event.py:L48 | neighbors=[SearchEventRepository, .export_events_csv(), .export_metrics_summary()] | lang=en
- "routers_metrics_parse_iso_dt": "_parse_iso_dt()" | kind=code-symbol | source=src/routers/metrics.py:L14 | neighbors=[metrics.py, export_csv(), summary()] | lang=en
- "routers_text_uploaders_copy": "text_uploaders copy.py" | kind=code-symbol | source=src/routers/text_uploaders copy.py:L1 | neighbors=[a7c7838 Initial commit: FastAPI AI sear…, get_response(), upload_phrase()] | lang=en
- "routers_user_queries_normalize_filters": "_normalize_filters()" | kind=code-symbol | source=src/routers/user_queries.py:L58 | neighbors=[user_queries.py, get_response(), _to_number_or_none()] | lang=en
- "routers_user_queries_normalize_response_block": "_normalize_response_block()" | kind=code-symbol | source=src/routers/user_queries.py:L42 | neighbors=[user_queries.py, get_response(), _to_number_or_none()] | lang=en
- "routers_user_queries_to_number_or_none": "_to_number_or_none()" | kind=code-symbol | source=src/routers/user_queries.py:L29 | neighbors=[user_queries.py, _normalize_filters(), _normalize_response_block()] | lang=en
- "scripts_eval_topk_aggregate": "aggregate()" | kind=code-symbol | source=scripts/eval_topk.py:L176 | neighbors=[eval_topk.py, percentile(), main()] | lang=en
- "text_generation_v1_v1": "V1" | kind=code-symbol | source=src/response_api/text_generation/v1.py:L8 | neighbors=[v1.py, .extract_search_intent(), .__init__()] | lang=en
- "text_generation_v2_debug_enabled": "_debug_enabled()" | kind=code-symbol | source=src/response_api/text_generation/v2.py:L17 | neighbors=[v2.py, .extract_search_intent(), .get_embedding_filter_by_attributes()] | lang=en
- "text_generation_v2_generatorv2_extract_search_intent": ".extract_search_intent()" | kind=code-symbol | source=src/response_api/text_generation/v2.py:L36 | neighbors=[GeneratorV2, _debug_enabled(), .clear_model_response()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /home/edgar/projects/pythonProjects/fastApi1/.graphify/description-instructions/batch-001.json

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
