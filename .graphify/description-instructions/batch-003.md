# Node Description Batch 4 of 7

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

- "models_contracts_chatturnin": "ChatTurnIn" | kind=code-symbol | source=src/models/contracts.py:L153 | neighbors=[contracts.py, StrictBaseModel]
- "models_contracts_chatturnout": "ChatTurnOut" | kind=code-symbol | source=src/models/contracts.py:L171 | neighbors=[contracts.py, StrictBaseModel]
- "models_contracts_correctioncreate": "CorrectionCreate" | kind=code-symbol | source=src/models/contracts.py:L16 | neighbors=[contracts.py, StrictBaseModel]
- "models_contracts_correctionupdate": "CorrectionUpdate" | kind=code-symbol | source=src/models/contracts.py:L30 | neighbors=[contracts.py, StrictBaseModel]
- "models_contracts_retrievalattributeout": "RetrievalAttributeOut" | kind=code-symbol | source=src/models/contracts.py:L98 | neighbors=[contracts.py, StrictBaseModel]
- "models_contracts_retrievalcandidateout": "RetrievalCandidateOut" | kind=code-symbol | source=src/models/contracts.py:L68 | neighbors=[contracts.py, StrictBaseModel]
- "models_contracts_retrievalconfidenceout": "RetrievalConfidenceOut" | kind=code-symbol | source=src/models/contracts.py:L78 | neighbors=[contracts.py, StrictBaseModel]
- "models_contracts_retrievalout": "RetrievalOut" | kind=code-symbol | source=src/models/contracts.py:L106 | neighbors=[contracts.py, StrictBaseModel]
- "models_contracts_retrievalrerankout": "RetrievalRerankOut" | kind=code-symbol | source=src/models/contracts.py:L91 | neighbors=[contracts.py, StrictBaseModel]
- "models_contracts_retrievalrerankweightsout": "RetrievalRerankWeightsOut" | kind=code-symbol | source=src/models/contracts.py:L85 | neighbors=[contracts.py, StrictBaseModel]
- "models_contracts_searcheventin": "SearchEventIn" | kind=code-symbol | source=src/models/contracts.py:L42 | neighbors=[contracts.py, StrictBaseModel]
- "models_contracts_searchintentresponse": "SearchIntentResponse" | kind=code-symbol | source=src/models/contracts.py:L58 | neighbors=[contracts.py, StrictBaseModel]
- "models_contracts_searchresponsemeta": "SearchResponseMeta" | kind=code-symbol | source=src/models/contracts.py:L125 | neighbors=[contracts.py, StrictBaseModel]
- "models_contracts_searchresponseout": "SearchResponseOut" | kind=code-symbol | source=src/models/contracts.py:L142 | neighbors=[contracts.py, StrictBaseModel]
- "models_corrections_appliedcorrection": "AppliedCorrection" | kind=code-symbol | source=src/models/corrections.py:L13 | neighbors=[corrections.py, GenericPostgresql]
- "models_corrections_correctionsrepository_list_corrections": ".list_corrections()" | kind=code-symbol | source=src/models/corrections.py:L37 | neighbors=[CorrectionsRepository, .apply_corrections()]
- "models_corrections_correctionsrepository_normalize": "._normalize()" | kind=code-symbol | source=src/models/corrections.py:L32 | neighbors=[CorrectionsRepository, ._matches()]
- "models_embedded_phrase_base_embeddedphraseuploadbase": "EmbeddedPhraseUploadBase" | kind=code-symbol | source=src/models/embedded_phrase_base.py:L11 | neighbors=[embedded_phrase_base.py, BaseModel]
- "models_embedded_phrase_embeddedphrase_extract_client_suffix": "._extract_client_suffix()" | kind=code-symbol | source=src/models/embedded_phrase.py:L366 | neighbors=[EmbeddedPhrase, ._select_row_for_scope()]
- "models_embedded_phrase_embeddedphrase_normalize_phrase_text": "._normalize_phrase_text()" | kind=code-symbol | source=src/models/embedded_phrase.py:L357 | neighbors=[EmbeddedPhrase, ._select_row_for_scope()]
- "models_embedded_phrase_embeddedphrase_resolve_business_boost": "._resolve_business_boost()" | kind=code-symbol | source=src/models/embedded_phrase.py:L569 | neighbors=[EmbeddedPhrase, ._select_row_for_scope()]
- "models_embedded_phrase_embeddedphrase_scope_part": "._scope_part()" | kind=code-symbol | source=src/models/embedded_phrase.py:L374 | neighbors=[EmbeddedPhrase, ._scoped_env_names()]
- "models_embedded_phrase_embeddedphrase_select_row": ".select_row()" | kind=code-symbol | source=src/models/embedded_phrase.py:L82 | neighbors=[EmbeddedPhrase, .select_row_with_diagnostics()]
- "models_embedded_phrase_rationale_54": "# TODO: this function may change, and use the class properties instead of receiv" | kind=entity | source=src/models/embedded_phrase.py:L54 | neighbors=[embedded_phrase.py, GenericPostgresql]
- "models_embedded_phrase_rationale_60": "# TODO: this function may change, and use the class properties instead of receiv" | kind=entity | source=src/models/embedded_phrase.py:L60 | neighbors=[embedded_phrase.py, GenericPostgresql]
- "models_generic_postgresql_env": "_env()" | kind=code-symbol | source=src/models/generic_postgresql.py:L14 | neighbors=[generic_postgresql.py, .__init__()]
- "models_generic_postgresql_genericpostgresql_execute_select": ".execute_select()" | kind=code-symbol | source=src/models/generic_postgresql.py:L65 | neighbors=[GenericPostgresql, .get_connection()]
- "models_generic_postgresql_genericpostgresql_init": ".__init__()" | kind=code-symbol | source=src/models/generic_postgresql.py:L25 | neighbors=[GenericPostgresql, _env()]
- "models_generic_postgresql_genericpostgresql_insert_single_row": ".insert_single_row()" | kind=code-symbol | source=src/models/generic_postgresql.py:L50 | neighbors=[GenericPostgresql, .get_connection()]
- "models_query_rules_queryrulesresolver_scope_part": "._scope_part()" | kind=code-symbol | source=src/models/query_rules.py:L39 | neighbors=[QueryRulesResolver, ._scoped_env_names()]
- "models_query_rules_redirectmatch_to_dict": ".to_dict()" | kind=code-symbol | source=src/models/query_rules.py:L17 | neighbors=[.resolve(), RedirectMatch]
- "models_search_event": "search_event.py" | kind=code-symbol | source=src/models/search_event.py:L1 | neighbors=[a7c7838 Initial commit: FastAPI AI sear…, SearchEventRepository]
- "models_search_event_searcheventrepository_export_events_csv": ".export_events_csv()" | kind=code-symbol | source=src/models/search_event.py:L128 | neighbors=[SearchEventRepository, ._build_where()]
- "models_search_event_searcheventrepository_export_metrics_summary": ".export_metrics_summary()" | kind=code-symbol | source=src/models/search_event.py:L54 | neighbors=[SearchEventRepository, ._build_where()]
- "postgresql_connector_env": "_env()" | kind=code-symbol | source=src/dbpersistence/postgresql/connector.py:L15 | neighbors=[connector.py, .__init__()]
- "postgresql_connector_postgresqlconnector_get_connection": ".get_connection()" | kind=code-symbol | source=src/dbpersistence/postgresql/connector.py:L46 | neighbors=[PostgreSqlConnector, .insert_single_row()]
- "postgresql_connector_postgresqlconnector_init": ".__init__()" | kind=code-symbol | source=src/dbpersistence/postgresql/connector.py:L26 | neighbors=[PostgreSqlConnector, _env()]
- "postgresql_connector_postgresqlconnector_insert_single_row": ".insert_single_row()" | kind=code-symbol | source=src/dbpersistence/postgresql/connector.py:L54 | neighbors=[PostgreSqlConnector, .get_connection()]
- "response_api_openai_embedder": "openai_embedder.py" | kind=code-symbol | source=src/response_api/openai_embedder.py:L1 | neighbors=[a7c7838 Initial commit: FastAPI AI sear…, OpenAIEmbedder]
- "routers_chat_turn_chat_turn": "chat_turn()" | kind=code-symbol | source=src/routers/chat_turn.py:L415 | neighbors=[chat_turn.py, _handle_chat_turn()]

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
