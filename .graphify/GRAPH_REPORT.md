# Graph Report - .  (2026-07-28)

## Corpus Check
- Corpus is ~35,095 words - fits in a single context window. You may not need a graph.

## Summary
- 179 nodes · 321 edges · 11 communities detected
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 9 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output
- Edge kinds: contains: 70 · MODIFIES: 68 · calls: 62 · method: 52 · ON_BRANCH: 20 · inherits: 19 · PARENT_OF: 19 · uses: 9 · rationale_for: 2


## Input Scope
- Requested: auto
- Resolved: committed (source: default-auto)
- Included files: 41 · Candidates: 94
- Excluded: 14 untracked · 5902 ignored · 0 sensitive · 0 missing committed
- Recommendation: Use --scope all or graphify.yaml inputs.corpus for a knowledge-base folder.

## Graph Freshness
- Built from Git commit: `7c5f9ce`
- Compare this hash to `git rev-parse HEAD` before trusting freshness-sensitive graph output.
## God Nodes (most connected - your core abstractions)
1. `StrictBaseModel` - 15 edges
2. `EmbeddedPhrase` - 15 edges
3. `CorrectionsRepository` - 12 edges
4. `GenericPostgresql` - 12 edges
5. `QueryRulesResolver` - 11 edges
6. `main()` - 9 edges
7. `SearchEventRepository` - 7 edges
8. `GeneratorV2` - 7 edges
9. `PostgreSqlConnector` - 6 edges
10. `DuplicateActiveCorrectionError` - 6 edges

## Surprising Connections (you probably didn't know these)
- `AppliedCorrection` --uses--> `GenericPostgresql`  [INFERRED]
  src/models/corrections.py → src/models/generic_postgresql.py
- `CorrectionsRepository` --uses--> `GenericPostgresql`  [INFERRED]
  src/models/corrections.py → src/models/generic_postgresql.py
- `DuplicateActiveCorrectionError` --uses--> `GenericPostgresql`  [INFERRED]
  src/models/corrections.py → src/models/generic_postgresql.py
- `EmbeddedPhrase` --uses--> `GenericPostgresql`  [INFERRED]
  src/models/embedded_phrase.py → src/models/generic_postgresql.py
- `# TODO: this function may change, and use the class properties instead of receiv` --uses--> `GenericPostgresql`  [INFERRED]
  src/models/embedded_phrase.py → src/models/generic_postgresql.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.06
Nodes (4): public.embedded_phrase, V1, 5d6519d Enforce active correction uniqueness in API and DB docs, a7c7838 Initial commit: FastAPI AI search backend docs and source

### Community 1 - "Community 1"
Cohesion: 0.15
Nodes (23): _to_number_or_none(), _normalize_response_block(), _normalize_filters(), _to_int(), _empty_retrieval(), _load_attribute_min_similarity(), get_response(), 3b16823 Fallback to legacy default embedding scope (+15 more)

### Community 6 - "Community 6"
Cohesion: 0.29
Nodes (12): EvalRow, parse_args(), _as_number_or_none(), load_queries(), fetch_json(), parse_eval_row(), build_call_url(), aggregate() (+4 more)

### Community 2 - "Community 2"
Cohesion: 0.15
Nodes (8): _env(), PostgreSqlConnector, # TODO: this function may change, and use the class properties instead of receiv, _env(), GenericPostgresql, 26dec16 fix to get correct credencials, 97b6afa fix to get correct credencials v2, e630bec fix to get correct credencials v3

### Community 3 - "Community 3"
Cohesion: 0.20
Nodes (16): StrictBaseModel, BaseModel, CorrectionCreate, CorrectionUpdate, SearchEventIn, SearchIntentResponse, RetrievalCandidateOut, RetrievalConfidenceOut (+8 more)

### Community 4 - "Community 4"
Cohesion: 0.24
Nodes (4): AppliedCorrection, DuplicateActiveCorrectionError, Exception, CorrectionsRepository

### Community 9 - "Community 9"
Cohesion: 0.38
Nodes (2): GenericPostgresql, SearchEventRepository

### Community 7 - "Community 7"
Cohesion: 0.29
Nodes (1): EmbeddedPhrase

### Community 5 - "Community 5"
Cohesion: 0.29
Nodes (3): RedirectMatch, QueryRulesResolver, Resuelve stopwords y redirects por scope multi-commerce.      Env vars soportada

### Community 8 - "Community 8"
Cohesion: 0.22
Nodes (3): OpenAIEmbedder, _debug_enabled(), GeneratorV2

### Community 10 - "Community 10"
Cohesion: 0.60
Nodes (3): _parse_iso_dt(), summary(), export_csv()

## Knowledge Gaps
- **2 isolated node(s):** `public.embedded_phrase`, `Resuelve stopwords y redirects por scope multi-commerce.      Env vars soportada`
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 9`** (2 nodes): `GenericPostgresql`, `SearchEventRepository`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 7`** (1 nodes): `EmbeddedPhrase`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `EmbeddedPhrase` connect `Community 7` to `Community 1`, `Community 9`, `Community 2`, `Community 8`?**
  _High betweenness centrality (0.167) - this node is a cross-community bridge._
- **Why does `GenericPostgresql` connect `Community 2` to `Community 4`, `Community 7`, `Community 9`?**
  _High betweenness centrality (0.130) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `EmbeddedPhrase` (e.g. with `GenericPostgresql` and `GeneratorV2`) actually correct?**
  _`EmbeddedPhrase` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `public.embedded_phrase`, `Resuelve stopwords y redirects por scope multi-commerce.      Env vars soportada` to the rest of the system?**
  _2 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.06060606060606061 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.14942528735632185 - nodes in this community are weakly interconnected._