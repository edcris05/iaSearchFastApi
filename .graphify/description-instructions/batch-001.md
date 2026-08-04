# Node Description Batch 2 of 7

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

- "commit:repo:github.com/edcris05/iaSearchFastApi@26dec16627a8dfc5ca12863e3cad9c19f7421338": "26dec16 fix to get correct credencials" | kind=Commit | source=git | neighbors=[main, 97b6afa fix to get correct credencials …, generic_postgresql.py, connector.py, d46099c add log to trace] | lang=en
- "commit:repo:github.com/edcris05/iaSearchFastApi@97871081e5b876e3a8ff823335083e8500c07393": "9787108 add rerank" | kind=Commit | source=git | neighbors=[main, dc7cc56 add script to swith with severa…, contracts.py, embedded_phrase.py, cda8c70 fixes v1] | lang=en
- "commit:repo:github.com/edcris05/iaSearchFastApi@97b6afadb51a877a0aec88d3846ce48e2c211271": "97b6afa fix to get correct credencials v2" | kind=Commit | source=git | neighbors=[26dec16 fix to get correct credencials, main, e630bec fix to get correct credencials …, generic_postgresql.py, connector.py] | lang=en
- "commit:repo:github.com/edcris05/iaSearchFastApi@c38131ed42aa16178483493d342f58a054a3119f": "c38131e Document embedded phrase scope backfill" | kind=Commit | source=git | neighbors=[3b16823 Fallback to legacy default embe…, main, ffd8c5f Protect admin endpoints and for…, embedded_phrase.py, 003_embedded_phrase_backfill_movistar_b…] | lang=en
- "commit:repo:github.com/edcris05/iaSearchFastApi@d46099c9486d65339ad55e22a284271832bb6de3": "d46099c add log to trace" | kind=Commit | source=git | neighbors=[main, 26dec16 fix to get correct credencials, user_queries.py, v2.py, dc7cc56 add script to swith with severa…] | lang=en
- "models_corrections_correctionsrepository_update_correction": ".update_correction()" | kind=code-symbol | source=src/models/corrections.py:L238 | neighbors=[CorrectionsRepository, .deactivate_correction(), ._find_active_duplicate_id(), ._write_audit(), DuplicateActiveCorrectionError] | lang=en
- "models_query_rules_queryrulesresolver_normalize_text": "._normalize_text()" | kind=code-symbol | source=src/models/query_rules.py:L69 | neighbors=[QueryRulesResolver, .apply_stopwords(), ._extract_redirects(), ._extract_stopwords(), .match_redirect()] | lang=en
- "response_api_openai_embedder_openaiembedder": "OpenAIEmbedder" | kind=code-symbol | source=src/response_api/openai_embedder.py:L25 | neighbors=[openai_embedder.py, .get_embedding(), .__init__(), .__repr__(), GeneratorV2] | lang=en
- "routers_chat_turn_flatten_filters": "_flatten_filters()" | kind=code-symbol | source=src/routers/chat_turn.py:L66 | neighbors=[chat_turn.py, _detect_intent(), _filters_to_human_text(), _handle_chat_turn(), _merge_filters()] | lang=en
- "src_main": "main.py" | kind=code-symbol | source=src/main.py:L1 | neighbors=[1a1a6aa add logs, a7c7838 Initial commit: FastAPI AI sear…, b599c82 add chat turns, home(), list_routes()] | lang=en
- "tests_test_scope_config_scopeconfigtests": "ScopeConfigTests" | kind=code-symbol | source=tests/test_scope_config.py:L7 | neighbors=[test_scope_config.py, .setUp(), .tearDown(), .test_resolve_scoped_env_prefers_most_s…, .test_scoped_env_names_build_expected_h…] | lang=en
- "commit:repo:github.com/edcris05/iaSearchFastApi@3786eb28e31ccc9196ff81054a9bb0a503918e64": "3786eb2 fix: safe prompt rendering without str.format for JSON templates" | kind=Commit | source=git | neighbors=[main, fa52d27 fix: problems with zscaler, v2.py, 5417f49 fix after updates of generic st…] | lang=en
- "commit:repo:github.com/edcris05/iaSearchFastApi@3b1682376b15af3cd66918ae37658c6dfbf73a77": "3b16823 Fallback to legacy default embedding scope" | kind=Commit | source=git | neighbors=[main, c38131e Document embedded phrase scope …, embedded_phrase.py, 8e8d84e Scope embedded phrases by tenan…] | lang=en
- "commit:repo:github.com/edcris05/iaSearchFastApi@4aa3dd25091fd1c239b8c4f1e752cabc29a7d5ba": "4aa3dd2 fix ssl problem v3" | kind=Commit | source=git | neighbors=[main, 324741e fix: problems with chat voice, v2.py, aea8997 fix: problems with zscaler v2] | lang=en
- "commit:repo:github.com/edcris05/iaSearchFastApi@5417f49c4bb02d38fdd0a075d837cdb23c588f24": "5417f49 fix after updates of generic stuffs" | kind=Commit | source=git | neighbors=[main, 3786eb2 fix: safe prompt rendering with…, v2.py, dc0aeeb add graphify to gitignore] | lang=en
- "commit:repo:github.com/edcris05/iaSearchFastApi@5d1fb2112c83697600e126f1858820eaa7f08855": "5d1fb21 add rerank config" | kind=Commit | source=git | neighbors=[main, ac8404a changes after test re rank, embedded_phrase.py, e630bec fix to get correct credencials …] | lang=en
- "commit:repo:github.com/edcris05/iaSearchFastApi@7c5f9cedc985dbef96f3a4b6bf87daf210c604eb": "7c5f9ce fixes for typo" | kind=Commit | source=git | neighbors=[main, 8ac887c update graphify, embedded_phrase.py, b5ddc30 fixes when we use the phrases i…] | lang=en
- "commit:repo:github.com/edcris05/iaSearchFastApi@ac8404a18ccec5125ce23ecddf3a6a5ee8d511e5": "ac8404a changes after test re rank" | kind=Commit | source=git | neighbors=[5d1fb21 add rerank config, main, d3311b3 add graphify, eval_topk.py] | lang=pt
- "commit:repo:github.com/edcris05/iaSearchFastApi@aea8997b26eb453f00f718bf9c87f7b163e81e2e": "aea8997 fix: problems with zscaler v2" | kind=Commit | source=git | neighbors=[main, 4aa3dd2 fix ssl problem v3, v2.py, fa52d27 fix: problems with zscaler] | lang=en
- "commit:repo:github.com/edcris05/iaSearchFastApi@cda8c7092d9d22167ab6d00bb9f615af07cf8593": "cda8c70 fixes v1" | kind=Commit | source=git | neighbors=[7be5620 feat: add top-k retrieval diagn…, main, 9787108 add rerank, user_queries.py] | lang=en
- "commit:repo:github.com/edcris05/iaSearchFastApi@fa52d2776ff55843d7d7d9686713f314f1c52497": "fa52d27 fix: problems with zscaler" | kind=Commit | source=git | neighbors=[3786eb2 fix: safe prompt rendering with…, main, aea8997 fix: problems with zscaler v2, v2.py] | lang=en
- "genericpostgresql": "GenericPostgresql" | kind=code-symbol | neighbors=[ChatSessionContextRepository, CorrectionsRepository, EmbeddedPhrase, SearchEventRepository] | lang=en
- "models_corrections_correctionsrepository_create_correction": ".create_correction()" | kind=code-symbol | source=src/models/corrections.py:L156 | neighbors=[CorrectionsRepository, ._find_active_duplicate_id(), ._write_audit(), DuplicateActiveCorrectionError] | lang=en
- "models_corrections_correctionsrepository_write_audit": "._write_audit()" | kind=code-symbol | source=src/models/corrections.py:L95 | neighbors=[CorrectionsRepository, .create_correction(), .deactivate_correction(), .update_correction()] | lang=en
- "models_embedded_phrase_base": "embedded_phrase_base.py" | kind=code-symbol | source=src/models/embedded_phrase_base.py:L1 | neighbors=[050dc6f feat: generic scope/domain prof…, 8e8d84e Scope embedded phrases by tenan…, a7c7838 Initial commit: FastAPI AI sear…, EmbeddedPhraseUploadBase] | lang=en
- "models_embedded_phrase_embeddedphrase_parse_scoped_json_env": "._parse_scoped_json_env()" | kind=code-symbol | source=src/models/embedded_phrase.py:L405 | neighbors=[EmbeddedPhrase, ._load_attr_min_margin(), ._load_attr_min_similarity_delta(), ._scoped_env_names()] | lang=en
- "models_embedded_phrase_embeddedphrase_scoped_env_names": "._scoped_env_names()" | kind=code-symbol | source=src/models/embedded_phrase.py:L384 | neighbors=[EmbeddedPhrase, ._load_rerank_config(), ._parse_scoped_json_env(), ._scope_part()] | lang=en
- "models_query_rules_queryrulesresolver_match_redirect": ".match_redirect()" | kind=code-symbol | source=src/models/query_rules.py:L194 | neighbors=[QueryRulesResolver, ._normalize_text(), RedirectMatch, .resolve()] | lang=en
- "routers_chat_turn_merge_filters": "_merge_filters()" | kind=code-symbol | source=src/routers/chat_turn.py:L134 | neighbors=[chat_turn.py, _handle_chat_turn(), _flatten_filters(), _group_flat_filters()] | lang=en
- "routers_text_uploaders": "text_uploaders.py" | kind=code-symbol | source=src/routers/text_uploaders.py:L1 | neighbors=[8e8d84e Scope embedded phrases by tenan…, a7c7838 Initial commit: FastAPI AI sear…, get_response(), upload_phrase()] | lang=en
- "routers_text_uploaders_copy_2": "text_uploaders copy 2.py" | kind=code-symbol | source=src/routers/text_uploaders copy 2.py:L1 | neighbors=[a7c7838 Initial commit: FastAPI AI sear…, get_response(), upload_csv(), upload_phrase()] | lang=en
- "scripts_eval_topk_parse_eval_row": "parse_eval_row()" | kind=code-symbol | source=scripts/eval_topk.py:L114 | neighbors=[eval_topk.py, main(), _as_number_or_none(), EvalRow] | lang=en
- "utils_domain_profile": "domain_profile.py" | kind=code-symbol | source=src/utils/domain_profile.py:L1 | neighbors=[050dc6f feat: generic scope/domain prof…, normalize_domain_profile(), resolve_domain_profile(), resolve_numeric_aliases()] | lang=en
- "utils_intent_normalization": "intent_normalization.py" | kind=code-symbol | source=src/utils/intent_normalization.py:L1 | neighbors=[050dc6f feat: generic scope/domain prof…, _first_numeric(), normalize_response_block(), to_number_or_none()] | lang=en
- "utils_scope_config": "scope_config.py" | kind=code-symbol | source=src/utils/scope_config.py:L1 | neighbors=[050dc6f feat: generic scope/domain prof…, resolve_scoped_env(), _scope_part(), scoped_env_names()] | lang=en
- "commit:repo:github.com/edcris05/iaSearchFastApi@324741ee2016e4fec31ee67ce10e64ebe4abe842": "324741e fix: problems with chat voice" | kind=Commit | source=git | neighbors=[main, chat_turn.py, 4aa3dd2 fix ssl problem v3] | lang=en
- "commit:repo:github.com/edcris05/iaSearchFastApi@8ac887c7dc04e569fe6ad78fee19f37c5beb362a": "8ac887c update graphify" | kind=Commit | source=git | neighbors=[7c5f9ce fixes for typo, main, b599c82 add chat turns] | lang=en
- "commit:repo:github.com/edcris05/iaSearchFastApi@d3311b34d04e5b997f56f9263d0c6242ffc2f86a": "d3311b3 add graphify" | kind=Commit | source=git | neighbors=[ac8404a changes after test re rank, main, 92f7548 adding redirects and stopwords] | lang=en
- "commit:repo:github.com/edcris05/iaSearchFastApi@dc0aeeb400c6a38968a2e036491761fd30dbfee0": "dc0aeeb add graphify to gitignore" | kind=Commit | source=git | neighbors=[050dc6f feat: generic scope/domain prof…, main, 5417f49 fix after updates of generic st…] | lang=en
- "commit:repo:github.com/edcris05/iaSearchFastApi@dc7cc5679a5f59cf86ccc0885023da890f64be06": "dc7cc56 add script to swith with several profiles" | kind=Commit | source=git | neighbors=[9787108 add rerank, main, d46099c add log to trace] | lang=en

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
