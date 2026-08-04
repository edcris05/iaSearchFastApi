# Node Description Batch 5 of 7

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

- "routers_chat_turn_chat_turn_no_trailing_slash": "chat_turn_no_trailing_slash()" | kind=code-symbol | source=src/routers/chat_turn.py:L420 | neighbors=[chat_turn.py, _handle_chat_turn()]
- "routers_chat_turn_detect_operation": "_detect_operation()" | kind=code-symbol | source=src/routers/chat_turn.py:L82 | neighbors=[chat_turn.py, _handle_chat_turn()]
- "routers_chat_turn_group_flat_filters": "_group_flat_filters()" | kind=code-symbol | source=src/routers/chat_turn.py:L75 | neighbors=[chat_turn.py, _merge_filters()]
- "routers_chat_turn_looks_like_new_search": "_looks_like_new_search()" | kind=code-symbol | source=src/routers/chat_turn.py:L102 | neighbors=[chat_turn.py, _handle_chat_turn()]
- "routers_chat_turn_normalize_search_text": "_normalize_search_text()" | kind=code-symbol | source=src/routers/chat_turn.py:L237 | neighbors=[chat_turn.py, _build_search_text()]
- "routers_chat_turn_to_number_or_none": "_to_number_or_none()" | kind=code-symbol | source=src/routers/chat_turn.py:L15 | neighbors=[chat_turn.py, _normalize_filters()]
- "routers_metrics_export_csv": "export_csv()" | kind=code-symbol | source=src/routers/metrics.py:L45 | neighbors=[metrics.py, _parse_iso_dt()]
- "routers_metrics_summary": "summary()" | kind=code-symbol | source=src/routers/metrics.py:L29 | neighbors=[metrics.py, _parse_iso_dt()]
- "routers_user_queries_empty_retrieval": "_empty_retrieval()" | kind=code-symbol | source=src/routers/user_queries.py:L93 | neighbors=[user_queries.py, get_response()]
- "routers_user_queries_load_attribute_min_similarity": "_load_attribute_min_similarity()" | kind=code-symbol | source=src/routers/user_queries.py:L102 | neighbors=[user_queries.py, get_response()]
- "routers_user_queries_to_int": "_to_int()" | kind=code-symbol | source=src/routers/user_queries.py:L86 | neighbors=[user_queries.py, get_response()]
- "scripts_eval_topk_as_number_or_none": "_as_number_or_none()" | kind=code-symbol | source=scripts/eval_topk.py:L63 | neighbors=[eval_topk.py, parse_eval_row()]
- "scripts_eval_topk_build_call_url": "build_call_url()" | kind=code-symbol | source=scripts/eval_topk.py:L163 | neighbors=[eval_topk.py, main()]
- "scripts_eval_topk_compare_to_baseline": "compare_to_baseline()" | kind=code-symbol | source=scripts/eval_topk.py:L227 | neighbors=[eval_topk.py, main()]
- "scripts_eval_topk_evalrow": "EvalRow" | kind=code-symbol | source=scripts/eval_topk.py:L28 | neighbors=[eval_topk.py, parse_eval_row()]
- "scripts_eval_topk_fetch_json": "fetch_json()" | kind=code-symbol | source=scripts/eval_topk.py:L92 | neighbors=[eval_topk.py, main()]
- "scripts_eval_topk_load_queries": "load_queries()" | kind=code-symbol | source=scripts/eval_topk.py:L77 | neighbors=[eval_topk.py, main()]
- "scripts_eval_topk_parse_args": "parse_args()" | kind=code-symbol | source=scripts/eval_topk.py:L46 | neighbors=[eval_topk.py, main()]
- "scripts_eval_topk_percentile": "percentile()" | kind=code-symbol | source=scripts/eval_topk.py:L214 | neighbors=[eval_topk.py, aggregate()]
- "scripts_eval_topk_write_raw_csv": "write_raw_csv()" | kind=code-symbol | source=scripts/eval_topk.py:L277 | neighbors=[eval_topk.py, main()]
- "tests_test_domain_profile_contract": "test_domain_profile_contract.py" | kind=code-symbol | source=tests/test_domain_profile_contract.py:L1 | neighbors=[050dc6f feat: generic scope/domain prof…, DomainProfileContractTests]
- "tests_test_scope_config": "test_scope_config.py" | kind=code-symbol | source=tests/test_scope_config.py:L1 | neighbors=[050dc6f feat: generic scope/domain prof…, ScopeConfigTests]
- "text_generation_v1": "v1.py" | kind=code-symbol | source=src/response_api/text_generation/v1.py:L1 | neighbors=[a7c7838 Initial commit: FastAPI AI sear…, V1]
- "text_generation_v2_generatorv2_clear_model_response": ".clear_model_response()" | kind=code-symbol | source=src/response_api/text_generation/v2.py:L250 | neighbors=[GeneratorV2, .extract_search_intent()]
- "text_generation_v2_generatorv2_default_prompt_template": "._default_prompt_template()" | kind=code-symbol | source=src/response_api/text_generation/v2.py:L59 | neighbors=[GeneratorV2, ._resolve_prompt_template()]
- "text_generation_v2_generatorv2_get_embedding_filter_by_attributes": ".get_embedding_filter_by_attributes()" | kind=code-symbol | source=src/response_api/text_generation/v2.py:L255 | neighbors=[GeneratorV2, _debug_enabled()]
- "text_generation_v2_generatorv2_render_prompt": "._render_prompt()" | kind=code-symbol | source=src/response_api/text_generation/v2.py:L158 | neighbors=[GeneratorV2, .extract_search_intent()]
- "text_generation_v2_generatorv2_resolve_system_prompt": "._resolve_system_prompt()" | kind=code-symbol | source=src/response_api/text_generation/v2.py:L136 | neighbors=[GeneratorV2, .extract_search_intent()]
- "utils_auth": "auth.py" | kind=code-symbol | source=src/utils/auth.py:L1 | neighbors=[ffd8c5f Protect admin endpoints and for…, require_admin_api_key()]
- "utils_config": "config.py" | kind=code-symbol | source=src/utils/config.py:L1 | neighbors=[a7c7838 Initial commit: FastAPI AI sear…, get_openai_key()]
- "utils_domain_profile_normalize_domain_profile": "normalize_domain_profile()" | kind=code-symbol | source=src/utils/domain_profile.py:L11 | neighbors=[domain_profile.py, resolve_domain_profile()]
- "utils_domain_profile_resolve_domain_profile": "resolve_domain_profile()" | kind=code-symbol | source=src/utils/domain_profile.py:L18 | neighbors=[domain_profile.py, normalize_domain_profile()]
- "utils_scope_config_resolve_scoped_env": "resolve_scoped_env()" | kind=code-symbol | source=src/utils/scope_config.py:L43 | neighbors=[scope_config.py, scoped_env_names()]
- "utils_scope_config_scope_part": "_scope_part()" | kind=code-symbol | source=src/utils/scope_config.py:L10 | neighbors=[scope_config.py, scoped_env_names()]
- "dbpersistence_init": "__init__.py" | kind=code-symbol | source=src/dbpersistence/__init__.py:L1 | neighbors=[a7c7838 Initial commit: FastAPI AI sear…]
- "embedded_phrase_public_embedded_phrase": "public.embedded_phrase" | kind=code-symbol | source=embedded_phrase.sql:L29 | neighbors=[embedded_phrase.sql]
- "exception": "Exception" | kind=code-symbol | neighbors=[DuplicateActiveCorrectionError]
- "models_chat_session_context_chatsessioncontextrepository_ensure_table": ".ensure_table()" | kind=code-symbol | source=src/models/chat_session_context.py:L10 | neighbors=[ChatSessionContextRepository]
- "models_chat_session_context_chatsessioncontextrepository_load_context": ".load_context()" | kind=code-symbol | source=src/models/chat_session_context.py:L32 | neighbors=[ChatSessionContextRepository]
- "models_chat_session_context_chatsessioncontextrepository_reset_context": ".reset_context()" | kind=code-symbol | source=src/models/chat_session_context.py:L105 | neighbors=[ChatSessionContextRepository]

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
