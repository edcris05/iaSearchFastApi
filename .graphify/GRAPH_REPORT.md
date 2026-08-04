# Graph Report - .  (2026-08-04)

## Corpus Check
- Corpus is ~15,887 words - fits in a single context window. You may not need a graph.

## Summary
- 240 nodes · 433 edges · 17 communities detected
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 11 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output
- Edge kinds: contains: 100 · calls: 88 · MODIFIES: 88 · method: 69 · ON_BRANCH: 26 · PARENT_OF: 25 · inherits: 23 · uses: 11 · rationale_for: 3


## Input Scope
- Requested: auto
- Resolved: committed (source: default-auto)
- Included files: 43 · Candidates: 115
- Excluded: 0 untracked · 5986 ignored · 0 sensitive · 0 missing committed
- Recommendation: Use --scope all or graphify.yaml inputs.corpus for a knowledge-base folder.

## Graph Freshness
- Built from Git commit: `5417f49`
- Compare this hash to `git rev-parse HEAD` before trusting freshness-sensitive graph output.
## God Nodes (most connected - your core abstractions)
1. `StrictBaseModel` - 18 edges
2. `EmbeddedPhrase` - 15 edges
3. `GenericPostgresql` - 14 edges
4. `CorrectionsRepository` - 12 edges
5. `QueryRulesResolver` - 11 edges
6. `GeneratorV2` - 11 edges
7. `_handle_chat_turn()` - 10 edges
8. `main()` - 9 edges
9. `ChatSessionContextRepository` - 7 edges
10. `SearchEventRepository` - 7 edges

## Surprising Connections (you probably didn't know these)
- `AppliedCorrection` --uses--> `GenericPostgresql`  [INFERRED]
  src/models/corrections.py → src/models/generic_postgresql.py
- `ChatSessionContextRepository` --uses--> `GenericPostgresql`  [INFERRED]
  src/models/chat_session_context.py → src/models/generic_postgresql.py
- `CorrectionsRepository` --uses--> `GenericPostgresql`  [INFERRED]
  src/models/corrections.py → src/models/generic_postgresql.py
- `DuplicateActiveCorrectionError` --uses--> `GenericPostgresql`  [INFERRED]
  src/models/corrections.py → src/models/generic_postgresql.py
- `EmbeddedPhrase` --uses--> `GenericPostgresql`  [INFERRED]
  src/models/embedded_phrase.py → src/models/generic_postgresql.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.10
Nodes (28): main, 050dc6f feat: generic scope/domain profile for intent extraction + scope contract tests, 3b16823 Fallback to legacy default embedding scope, 5417f49 fix after updates of generic stuffs, 5d1fb21 add rerank config, 5d6519d Enforce active correction uniqueness in API and DB docs, 7be5620 feat: add top-k retrieval diagnostics and configurable attribute thresholds, 7c5f9ce fixes for typo (+20 more)

### Community 1 - "Community 1"
Cohesion: 0.07
Nodes (4): a7c7838 Initial commit: FastAPI AI search backend docs and source, public.embedded_phrase, OpenAIEmbedder, V1

### Community 2 - "Community 2"
Cohesion: 0.14
Nodes (9): 26dec16 fix to get correct credencials, 97b6afa fix to get correct credencials v2, e630bec fix to get correct credencials v3, # TODO: this function may change, and use the class properties instead of receiv, # TODO: this function may change, and use the class properties instead of receiv, _env(), GenericPostgresql, _env() (+1 more)

### Community 3 - "Community 3"
Cohesion: 0.18
Nodes (19): BaseModel, AppliedCorrectionOut, ChatContextOut, ChatTurnIn, ChatTurnOut, CorrectionCreate, CorrectionUpdate, RetrievalAttributeOut (+11 more)

### Community 4 - "Community 4"
Cohesion: 0.13
Nodes (5): 1a1a6aa add logs, b599c82 add chat turns, GenericPostgresql, ChatSessionContextRepository, SearchEventRepository

### Community 5 - "Community 5"
Cohesion: 0.24
Nodes (4): Exception, AppliedCorrection, CorrectionsRepository, DuplicateActiveCorrectionError

### Community 6 - "Community 6"
Cohesion: 0.29
Nodes (14): _build_explanation(), _build_search_text(), chat_turn(), chat_turn_no_trailing_slash(), _detect_intent(), _detect_operation(), _filters_to_human_text(), _flatten_filters() (+6 more)

### Community 7 - "Community 7"
Cohesion: 0.29
Nodes (3): QueryRulesResolver, Resuelve stopwords y redirects por scope multi-commerce.      Env vars soportada, RedirectMatch

### Community 8 - "Community 8"
Cohesion: 0.29
Nodes (12): aggregate(), _as_number_or_none(), build_call_url(), compare_to_baseline(), EvalRow, fetch_json(), load_queries(), main() (+4 more)

### Community 9 - "Community 9"
Cohesion: 0.29
Nodes (1): EmbeddedPhrase

### Community 10 - "Community 10"
Cohesion: 0.33
Nodes (2): _debug_enabled(), GeneratorV2

### Community 11 - "Community 11"
Cohesion: 0.29
Nodes (1): DomainProfileContractTests

### Community 12 - "Community 12"
Cohesion: 0.33
Nodes (1): ScopeConfigTests

### Community 13 - "Community 13"
Cohesion: 0.60
Nodes (3): export_csv(), _parse_iso_dt(), summary()

### Community 14 - "Community 14"
Cohesion: 0.67
Nodes (2): normalize_domain_profile(), resolve_domain_profile()

### Community 15 - "Community 15"
Cohesion: 1.00
Nodes (3): _first_numeric(), normalize_response_block(), to_number_or_none()

### Community 16 - "Community 16"
Cohesion: 0.83
Nodes (3): resolve_scoped_env(), _scope_part(), scoped_env_names()

## Knowledge Gaps
- **2 isolated node(s):** `public.embedded_phrase`, `Resuelve stopwords y redirects por scope multi-commerce.      Env vars soportada`
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 9`** (1 nodes): `EmbeddedPhrase`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 10`** (2 nodes): `_debug_enabled()`, `GeneratorV2`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 11`** (1 nodes): `DomainProfileContractTests`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 12`** (1 nodes): `ScopeConfigTests`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 14`** (2 nodes): `normalize_domain_profile()`, `resolve_domain_profile()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `EmbeddedPhrase` connect `Community 9` to `Community 0`, `Community 4`, `Community 2`, `Community 10`?**
  _High betweenness centrality (0.131) - this node is a cross-community bridge._
- **Why does `GenericPostgresql` connect `Community 2` to `Community 4`, `Community 5`, `Community 9`?**
  _High betweenness centrality (0.131) - this node is a cross-community bridge._
- **Why does `GeneratorV2` connect `Community 10` to `Community 0`, `Community 9`, `Community 1`?**
  _High betweenness centrality (0.082) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `EmbeddedPhrase` (e.g. with `GenericPostgresql` and `GeneratorV2`) actually correct?**
  _`EmbeddedPhrase` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `public.embedded_phrase`, `Resuelve stopwords y redirects por scope multi-commerce.      Env vars soportada` to the rest of the system?**
  _2 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.10220673635307782 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.06666666666666667 - nodes in this community are weakly interconnected._