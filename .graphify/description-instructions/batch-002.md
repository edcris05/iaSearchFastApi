# Node Description Batch 3 of 5

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

- "basemodel": "BaseModel" | kind=code-symbol | neighbors=[StrictBaseModel, EmbeddedPhraseUploadBase]
- "embedded_phrase": "embedded_phrase.sql" | kind=code-symbol | source=embedded_phrase.sql:L1 | neighbors=[a7c7838 Initial commit: FastAPI AI sear…, public.embedded_phrase]
- "models_contracts_appliedcorrectionout": "AppliedCorrectionOut" | kind=code-symbol | source=src/models/contracts.py:L105 | neighbors=[contracts.py, StrictBaseModel]
- "models_contracts_correctioncreate": "CorrectionCreate" | kind=code-symbol | source=src/models/contracts.py:L9 | neighbors=[contracts.py, StrictBaseModel]
- "models_contracts_correctionupdate": "CorrectionUpdate" | kind=code-symbol | source=src/models/contracts.py:L23 | neighbors=[contracts.py, StrictBaseModel]
- "models_contracts_retrievalattributeout": "RetrievalAttributeOut" | kind=code-symbol | source=src/models/contracts.py:L90 | neighbors=[contracts.py, StrictBaseModel]
- "models_contracts_retrievalcandidateout": "RetrievalCandidateOut" | kind=code-symbol | source=src/models/contracts.py:L60 | neighbors=[contracts.py, StrictBaseModel]
- "models_contracts_retrievalconfidenceout": "RetrievalConfidenceOut" | kind=code-symbol | source=src/models/contracts.py:L70 | neighbors=[contracts.py, StrictBaseModel]
- "models_contracts_retrievalout": "RetrievalOut" | kind=code-symbol | source=src/models/contracts.py:L98 | neighbors=[contracts.py, StrictBaseModel]
- "models_contracts_retrievalrerankout": "RetrievalRerankOut" | kind=code-symbol | source=src/models/contracts.py:L83 | neighbors=[contracts.py, StrictBaseModel]
- "models_contracts_retrievalrerankweightsout": "RetrievalRerankWeightsOut" | kind=code-symbol | source=src/models/contracts.py:L77 | neighbors=[contracts.py, StrictBaseModel]
- "models_contracts_searcheventin": "SearchEventIn" | kind=code-symbol | source=src/models/contracts.py:L35 | neighbors=[contracts.py, StrictBaseModel]
- "models_contracts_searchintentresponse": "SearchIntentResponse" | kind=code-symbol | source=src/models/contracts.py:L51 | neighbors=[contracts.py, StrictBaseModel]
- "models_contracts_searchresponsemeta": "SearchResponseMeta" | kind=code-symbol | source=src/models/contracts.py:L117 | neighbors=[contracts.py, StrictBaseModel]
- "models_contracts_searchresponseout": "SearchResponseOut" | kind=code-symbol | source=src/models/contracts.py:L133 | neighbors=[contracts.py, StrictBaseModel]
- "models_corrections_appliedcorrection": "AppliedCorrection" | kind=code-symbol | source=src/models/corrections.py:L12 | neighbors=[corrections.py, GenericPostgresql]
- "models_corrections_correctionsrepository_list_corrections": ".list_corrections()" | kind=code-symbol | source=src/models/corrections.py:L36 | neighbors=[CorrectionsRepository, .apply_corrections()]
- "models_corrections_correctionsrepository_normalize": "._normalize()" | kind=code-symbol | source=src/models/corrections.py:L31 | neighbors=[CorrectionsRepository, ._matches()]
- "models_embedded_phrase_base_embeddedphraseuploadbase": "EmbeddedPhraseUploadBase" | kind=code-symbol | source=src/models/embedded_phrase_base.py:L4 | neighbors=[embedded_phrase_base.py, BaseModel]
- "models_embedded_phrase_embeddedphrase_extract_client_suffix": "._extract_client_suffix()" | kind=code-symbol | source=src/models/embedded_phrase.py:L337 | neighbors=[EmbeddedPhrase, ._select_row_for_scope()]
- "models_embedded_phrase_embeddedphrase_normalize_phrase_text": "._normalize_phrase_text()" | kind=code-symbol | source=src/models/embedded_phrase.py:L328 | neighbors=[EmbeddedPhrase, ._select_row_for_scope()]
- "models_embedded_phrase_embeddedphrase_resolve_business_boost": "._resolve_business_boost()" | kind=code-symbol | source=src/models/embedded_phrase.py:L467 | neighbors=[EmbeddedPhrase, ._select_row_for_scope()]
- "models_embedded_phrase_embeddedphrase_scope_part": "._scope_part()" | kind=code-symbol | source=src/models/embedded_phrase.py:L345 | neighbors=[EmbeddedPhrase, ._scoped_env_names()]
- "models_embedded_phrase_embeddedphrase_select_row": ".select_row()" | kind=code-symbol | source=src/models/embedded_phrase.py:L76 | neighbors=[EmbeddedPhrase, .select_row_with_diagnostics()]
- "models_embedded_phrase_rationale_54": "# TODO: this function may change, and use the class properties instead of receiv" | kind=entity | source=src/models/embedded_phrase.py:L54 | neighbors=[embedded_phrase.py, GenericPostgresql]
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
- "routers_metrics_export_csv": "export_csv()" | kind=code-symbol | source=src/routers/metrics.py:L45 | neighbors=[metrics.py, _parse_iso_dt()]

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
