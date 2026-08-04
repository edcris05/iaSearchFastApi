# Community Labeling

Graphify is running in assistant/skill mode (no API key). You are the host
assistant (Claude Code / Codex / Gemini CLI). Read the community listing below
and write 2-5 word plain-language names for each.

## Language

LANGUAGE: each community line ends with a `[lang=…]` marker giving the
language of its source nodes. Write that community's name in EXACTLY that
language. Do not normalize every name to one common language.

## Communities

Community 0: main, 050dc6f feat: generic scope/domain profile for intent extrac, 324741e fix: problems with chat voice, 3786eb2 fix: safe prompt rendering without str.format for JS, 3b16823 Fallback to legacy default embedding scope, 4aa3dd2 fix ssl problem v3, 5417f49 fix after updates of generic stuffs, 5d1fb21 add rerank config, 5d6519d Enforce active correction uniqueness in API and DB d, 7be5620 feat: add top-k retrieval diagnostics and configurab, 7c5f9ce fixes for typo, 8ac887c update graphify [lang=en]
Community 1: a7c7838 Initial commit: FastAPI AI search backend docs and s, __init__.py, embedded_phrase.sql, public.embedded_phrase, openai_embedder.py, OpenAIEmbedder, .get_embedding(, .__init__(, .__repr__(, corrections.py, create_correction(, delete_correction( [lang=en]
Community 2: StrictBaseModel, BaseModel, contracts.py, AppliedCorrectionOut, ChatContextOut, ChatTurnIn, ChatTurnOut, CorrectionCreate, CorrectionUpdate, RetrievalAttributeOut, RetrievalCandidateOut, RetrievalConfidenceOut [lang=en]
Community 3: GenericPostgresql, 26dec16 fix to get correct credencials, 97b6afa fix to get correct credencials v2, e630bec fix to get correct credencials v3, # TODO: this function may change, and use the class properti, generic_postgresql.py, _env(, .execute_select(, .get_connection(, .__init__(, .insert_single_row(, _load_project_env( [lang=en]
Community 4: ChatSessionContextRepository, SearchEventRepository, 1a1a6aa add logs, b599c82 add chat turns, GenericPostgresql, chat_session_context.py, .ensure_table(, .load_context(, .reset_context(, .save_context(, search_event.py, ._build_where( [lang=pt]
Community 5: _handle_chat_turn(, chat_turn.py, _build_explanation(, _build_search_text(, chat_turn(, chat_turn_no_trailing_slash(, _detect_intent(, _detect_operation(, _filters_to_human_text(, _flatten_filters(, _group_flat_filters(, _looks_like_new_search( [lang=en]
Community 6: CorrectionsRepository, Exception, corrections.py, AppliedCorrection, .apply_corrections(, .create_correction(, .deactivate_correction(, ._find_active_duplicate_id(, .list_corrections(, ._matches(, ._normalize(, .update_correction( [lang=en]
Community 7: EmbeddedPhrase, ._extract_client_suffix(, .__init__(, .insert_row(, ._load_attr_min_margin(, ._load_attr_min_similarity_delta(, ._load_rerank_config(, ._normalize_phrase_text(, ._parse_scoped_json_env(, ._resolve_business_boost(, ._scope_part(, ._scoped_env_names( [lang=en]
Community 8: QueryRulesResolver, query_rules.py, .apply_stopwords(, ._extract_redirects(, ._extract_stopwords(, ._load_scoped_config(, .match_redirect(, ._normalize_text(, .resolve(, ._scope_part(, ._scoped_env_names(, Resuelve stopwords y redirects por scope multi-commerce.     [lang=es]
Community 9: main(, eval_topk.py, aggregate(, _as_number_or_none(, build_call_url(, compare_to_baseline(, EvalRow, fetch_json(, load_queries(, parse_args(, parse_eval_row(, percentile( [lang=en]
Community 10: GeneratorV2, _debug_enabled(, .clear_model_response(, ._default_prompt_template(, .extract_search_intent(, .get_embedding_filter_by_attributes(, .__init__(, ._render_prompt(, ._resolve_prompt_template(, ._resolve_system_prompt( [lang=en]
Community 11: test_domain_profile_contract.py, DomainProfileContractTests, .setUp(, .tearDown(, .test_domain_profile_scoped_override(, .test_normalize_domain_profile_fallback(, .test_normalize_response_uses_aliases_and_domain_filters( [lang=en]
Community 12: test_scope_config.py, ScopeConfigTests, .setUp(, .tearDown(, .test_resolve_scoped_env_prefers_most_specific_override(, .test_scoped_env_names_build_expected_hierarchy( [lang=en]
Community 13: domain_profile.py, normalize_domain_profile(, resolve_domain_profile(, resolve_numeric_aliases( [lang=en]
Community 14: intent_normalization.py, _first_numeric(, normalize_response_block(, to_number_or_none( [lang=en]
Community 15: scope_config.py, resolve_scoped_env(, _scope_part(, scoped_env_names( [lang=en]

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
