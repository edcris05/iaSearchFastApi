# Community Labeling

Graphify is running in assistant/skill mode (no API key). You are the host
assistant (Claude Code / Codex / Gemini CLI). Read the community listing below
and write 2-5 word plain-language names for each.

## Language

LANGUAGE: each community line ends with a `[lang=…]` marker giving the
language of its source nodes. Write that community's name in EXACTLY that
language. Do not normalize every name to one common language.

## Communities

Community 0: 5d6519d Enforce active correction uniqueness in API and DB d, a7c7838 Initial commit: FastAPI AI search backend docs and s, __init__.py, embedded_phrase.sql, public.embedded_phrase, corrections.py, create_correction(, delete_correction(, list_corrections(, update_correction(, text_uploaders.py, text_uploaders copy.py [lang=en]
Community 1: main, 3b16823 Fallback to legacy default embedding scope, 5d1fb21 add rerank config, 7be5620 feat: add top-k retrieval diagnostics and configurab, 7c5f9ce fixes for typo, 8e8d84e Scope embedded phrases by tenant and store, 92f7548 adding redirects and stopwords, 9787108 add rerank, ac8404a changes after test re rank, b5ddc30 fixes when we use the phrases import, c38131e Document embedded phrase scope backfill, cda8c70 fixes v1 [lang=en]
Community 2: GenericPostgresql, PostgreSqlConnector, 26dec16 fix to get correct credencials, 97b6afa fix to get correct credencials v2, e630bec fix to get correct credencials v3, # TODO: this function may change, and use the class properti, generic_postgresql.py, _env(, .execute_select(, .get_connection(, .__init__(, .insert_single_row( [lang=en]
Community 3: StrictBaseModel, BaseModel, contracts.py, AppliedCorrectionOut, CorrectionCreate, CorrectionUpdate, RetrievalAttributeOut, RetrievalCandidateOut, RetrievalConfidenceOut, RetrievalOut, RetrievalRerankOut, RetrievalRerankWeightsOut [lang=en]
Community 4: CorrectionsRepository, DuplicateActiveCorrectionError, Exception, corrections.py, AppliedCorrection, .apply_corrections(, .create_correction(, .deactivate_correction(, ._find_active_duplicate_id(, .list_corrections(, ._matches(, ._normalize( [lang=en]
Community 5: QueryRulesResolver, query_rules.py, .apply_stopwords(, ._extract_redirects(, ._extract_stopwords(, ._load_scoped_config(, .match_redirect(, ._normalize_text(, .resolve(, ._scope_part(, ._scoped_env_names(, Resuelve stopwords y redirects por scope multi-commerce.     [lang=es]
Community 6: main(, eval_topk.py, aggregate(, _as_number_or_none(, build_call_url(, compare_to_baseline(, EvalRow, fetch_json(, load_queries(, parse_args(, parse_eval_row(, percentile( [lang=en]
Community 7: EmbeddedPhrase, ._extract_client_suffix(, .__init__(, .insert_row(, ._load_rerank_config(, ._normalize_phrase_text(, ._resolve_business_boost(, ._scope_part(, ._scoped_env_names(, .select_row(, ._select_row_for_scope(, .select_row_with_diagnostics( [lang=en]
Community 8: GeneratorV2, openai_embedder.py, OpenAIEmbedder, .get_embedding(, .__init__(, .__repr__(, _debug_enabled(, .clear_model_response(, .extract_search_intent(, .get_embedding_filter_by_attributes( [lang=en]
Community 9: SearchEventRepository, GenericPostgresql, search_event.py, ._build_where(, .export_events_csv(, .export_metrics_summary(, .log_event( [lang=en]
Community 10: metrics.py, export_csv(, log_event(, _parse_iso_dt(, summary( [lang=en]

## Instructions

Write a single JSON object mapping each community id (as a string) to its
2-5 word name to: /home/edgar/projects/pythonProjects/fastApi1/.graphify/label-instructions/communities.json

Example:
```json
{
  "0": "Authentication Flow",
  "1": "Authentication Flow",
  "2": "Authentication Flow"
}
```

Then re-run `graphify update` (or `graphify label`) to ingest the names.
