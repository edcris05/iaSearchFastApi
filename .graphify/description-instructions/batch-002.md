# Node Description Batch 3 of 7

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

- "models_corrections_correctionsrepository_apply_corrections": ".apply_corrections()" | kind=code-symbol | source=src/models/corrections.py:L392 | neighbors=[CorrectionsRepository, .list_corrections(), ._matches()]
- "models_corrections_correctionsrepository_deactivate_correction": ".deactivate_correction()" | kind=code-symbol | source=src/models/corrections.py:L354 | neighbors=[CorrectionsRepository, .update_correction(), ._write_audit()]
- "models_corrections_correctionsrepository_find_active_duplicate_id": "._find_active_duplicate_id()" | kind=code-symbol | source=src/models/corrections.py:L123 | neighbors=[CorrectionsRepository, .create_correction(), .update_correction()]
- "models_corrections_correctionsrepository_matches": "._matches()" | kind=code-symbol | source=src/models/corrections.py:L367 | neighbors=[CorrectionsRepository, .apply_corrections(), ._normalize()]
- "models_embedded_phrase_embeddedphrase_load_attr_min_margin": "._load_attr_min_margin()" | kind=code-symbol | source=src/models/embedded_phrase.py:L428 | neighbors=[EmbeddedPhrase, ._parse_scoped_json_env(), ._select_row_for_scope()]
- "models_embedded_phrase_embeddedphrase_load_attr_min_similarity_delta": "._load_attr_min_similarity_delta()" | kind=code-symbol | source=src/models/embedded_phrase.py:L453 | neighbors=[EmbeddedPhrase, ._parse_scoped_json_env(), ._select_row_for_scope()]
- "models_embedded_phrase_embeddedphrase_load_rerank_config": "._load_rerank_config()" | kind=code-symbol | source=src/models/embedded_phrase.py:L478 | neighbors=[EmbeddedPhrase, ._scoped_env_names(), ._select_row_for_scope()]
- "models_embedded_phrase_embeddedphrase_select_row_with_diagnostics": ".select_row_with_diagnostics()" | kind=code-symbol | source=src/models/embedded_phrase.py:L105 | neighbors=[EmbeddedPhrase, .select_row(), ._select_row_for_scope()]
- "models_generic_postgresql_genericpostgresql_get_connection": ".get_connection()" | kind=code-symbol | source=src/models/generic_postgresql.py:L45 | neighbors=[GenericPostgresql, .execute_select(), .insert_single_row()]
- "models_query_rules": "query_rules.py" | kind=code-symbol | source=src/models/query_rules.py:L1 | neighbors=[92f7548 adding redirects and stopwords, QueryRulesResolver, RedirectMatch]
- "models_query_rules_queryrulesresolver_apply_stopwords": ".apply_stopwords()" | kind=code-symbol | source=src/models/query_rules.py:L168 | neighbors=[QueryRulesResolver, ._normalize_text(), .resolve()]
- "models_query_rules_queryrulesresolver_extract_redirects": "._extract_redirects()" | kind=code-symbol | source=src/models/query_rules.py:L120 | neighbors=[QueryRulesResolver, ._normalize_text(), .resolve()]
- "models_query_rules_queryrulesresolver_extract_stopwords": "._extract_stopwords()" | kind=code-symbol | source=src/models/query_rules.py:L107 | neighbors=[QueryRulesResolver, ._normalize_text(), .resolve()]
- "models_query_rules_queryrulesresolver_load_scoped_config": "._load_scoped_config()" | kind=code-symbol | source=src/models/query_rules.py:L78 | neighbors=[QueryRulesResolver, ._scoped_env_names(), .resolve()]
- "models_query_rules_queryrulesresolver_scoped_env_names": "._scoped_env_names()" | kind=code-symbol | source=src/models/query_rules.py:L49 | neighbors=[QueryRulesResolver, ._load_scoped_config(), ._scope_part()]
- "models_query_rules_redirectmatch": "RedirectMatch" | kind=code-symbol | source=src/models/query_rules.py:L10 | neighbors=[query_rules.py, .match_redirect(), .to_dict()]
- "models_search_event_searcheventrepository_build_where": "._build_where()" | kind=code-symbol | source=src/models/search_event.py:L48 | neighbors=[SearchEventRepository, .export_events_csv(), .export_metrics_summary()]
- "routers_chat_turn_build_explanation": "_build_explanation()" | kind=code-symbol | source=src/routers/chat_turn.py:L270 | neighbors=[chat_turn.py, _filters_to_human_text(), _handle_chat_turn()]
- "routers_chat_turn_build_search_text": "_build_search_text()" | kind=code-symbol | source=src/routers/chat_turn.py:L242 | neighbors=[chat_turn.py, _normalize_search_text(), _handle_chat_turn()]
- "routers_chat_turn_detect_intent": "_detect_intent()" | kind=code-symbol | source=src/routers/chat_turn.py:L197 | neighbors=[chat_turn.py, _flatten_filters(), _handle_chat_turn()]
- "routers_chat_turn_filters_to_human_text": "_filters_to_human_text()" | kind=code-symbol | source=src/routers/chat_turn.py:L213 | neighbors=[chat_turn.py, _build_explanation(), _flatten_filters()]
- "routers_chat_turn_normalize_filters": "_normalize_filters()" | kind=code-symbol | source=src/routers/chat_turn.py:L28 | neighbors=[chat_turn.py, _handle_chat_turn(), _to_number_or_none()]
- "routers_metrics_parse_iso_dt": "_parse_iso_dt()" | kind=code-symbol | source=src/routers/metrics.py:L14 | neighbors=[metrics.py, export_csv(), summary()]
- "routers_text_uploaders_copy": "text_uploaders copy.py" | kind=code-symbol | source=src/routers/text_uploaders copy.py:L1 | neighbors=[a7c7838 Initial commit: FastAPI AI sear…, get_response(), upload_phrase()]
- "routers_user_queries_normalize_filters": "_normalize_filters()" | kind=code-symbol | source=src/routers/user_queries.py:L48 | neighbors=[user_queries.py, get_response(), _to_number_or_none()]
- "routers_user_queries_normalize_response_block": "_normalize_response_block()" | kind=code-symbol | source=src/routers/user_queries.py:L42 | neighbors=[user_queries.py, get_response(), _to_number_or_none()]
- "routers_user_queries_to_number_or_none": "_to_number_or_none()" | kind=code-symbol | source=src/routers/user_queries.py:L35 | neighbors=[user_queries.py, _normalize_filters(), _normalize_response_block()]
- "scripts_eval_topk_aggregate": "aggregate()" | kind=code-symbol | source=scripts/eval_topk.py:L176 | neighbors=[eval_topk.py, percentile(), main()]
- "text_generation_v1_v1": "V1" | kind=code-symbol | source=src/response_api/text_generation/v1.py:L8 | neighbors=[v1.py, .extract_search_intent(), .__init__()]
- "text_generation_v2_debug_enabled": "_debug_enabled()" | kind=code-symbol | source=src/response_api/text_generation/v2.py:L26 | neighbors=[v2.py, .extract_search_intent(), .get_embedding_filter_by_attributes()]
- "text_generation_v2_generatorv2_resolve_prompt_template": "._resolve_prompt_template()" | kind=code-symbol | source=src/response_api/text_generation/v2.py:L118 | neighbors=[GeneratorV2, .extract_search_intent(), ._default_prompt_template()]
- "utils_intent_normalization_first_numeric": "_first_numeric()" | kind=code-symbol | source=src/utils/intent_normalization.py:L17 | neighbors=[intent_normalization.py, to_number_or_none(), normalize_response_block()]
- "utils_intent_normalization_normalize_response_block": "normalize_response_block()" | kind=code-symbol | source=src/utils/intent_normalization.py:L25 | neighbors=[intent_normalization.py, _first_numeric(), to_number_or_none()]
- "utils_intent_normalization_to_number_or_none": "to_number_or_none()" | kind=code-symbol | source=src/utils/intent_normalization.py:L4 | neighbors=[intent_normalization.py, _first_numeric(), normalize_response_block()]
- "utils_scope_config_scoped_env_names": "scoped_env_names()" | kind=code-symbol | source=src/utils/scope_config.py:L23 | neighbors=[scope_config.py, resolve_scoped_env(), _scope_part()]
- "basemodel": "BaseModel" | kind=code-symbol | neighbors=[StrictBaseModel, EmbeddedPhraseUploadBase]
- "embedded_phrase": "embedded_phrase.sql" | kind=code-symbol | source=embedded_phrase.sql:L1 | neighbors=[a7c7838 Initial commit: FastAPI AI sear…, public.embedded_phrase]
- "models_chat_session_context": "chat_session_context.py" | kind=code-symbol | source=src/models/chat_session_context.py:L1 | neighbors=[b599c82 add chat turns, ChatSessionContextRepository]
- "models_contracts_appliedcorrectionout": "AppliedCorrectionOut" | kind=code-symbol | source=src/models/contracts.py:L113 | neighbors=[contracts.py, StrictBaseModel]
- "models_contracts_chatcontextout": "ChatContextOut" | kind=code-symbol | source=src/models/contracts.py:L165 | neighbors=[contracts.py, StrictBaseModel]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /home/edgar/projects/pythonProjects/fastApi1/.graphify/description-instructions/batch-002.json

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
