# Graph Report - .  (2026-07-22)

## Corpus Check
- Corpus is ~9,407 words - fits in a single context window. You may not need a graph.

## Summary
- 137 nodes · 183 edges · 11 communities detected
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 9 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output
- Edge kinds: contains: 67 · calls: 47 · method: 40 · inherits: 19 · uses: 9 · rationale_for: 1


## Input Scope
- Requested: all
- Resolved: all (source: configured-default)
- Included files: 26 · Candidates: recursive
- Excluded: 0 untracked · 0 ignored · 0 sensitive · 0 missing committed

## Graph Freshness
- Built from Git commit: `ac8404a`
- Compare this hash to `git rev-parse HEAD` before trusting freshness-sensitive graph output.
## God Nodes (most connected - your core abstractions)
1. `StrictBaseModel` - 15 edges
2. `EmbeddedPhrase` - 13 edges
3. `CorrectionsRepository` - 12 edges
4. `GenericPostgresql` - 12 edges
5. `main()` - 9 edges
6. `SearchEventRepository` - 7 edges
7. `GeneratorV2` - 7 edges
8. `PostgreSqlConnector` - 6 edges
9. `DuplicateActiveCorrectionError` - 6 edges
10. `get_response()` - 6 edges

## Surprising Connections (you probably didn't know these)
- `AppliedCorrection` --uses--> `GenericPostgresql`  [INFERRED]
  src/models/corrections.py → src/models/generic_postgresql.py
- `# TODO: this function may change, and use the class properties instead of receiv` --uses--> `GenericPostgresql`  [INFERRED]
  src/models/embedded_phrase.py → src/models/generic_postgresql.py
- `CorrectionsRepository` --uses--> `GenericPostgresql`  [INFERRED]
  src/models/corrections.py → src/models/generic_postgresql.py
- `DuplicateActiveCorrectionError` --uses--> `GenericPostgresql`  [INFERRED]
  src/models/corrections.py → src/models/generic_postgresql.py
- `EmbeddedPhrase` --uses--> `GenericPostgresql`  [INFERRED]
  src/models/embedded_phrase.py → src/models/generic_postgresql.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.20
Nodes (16): BaseModel, AppliedCorrectionOut, CorrectionCreate, CorrectionUpdate, RetrievalAttributeOut, RetrievalCandidateOut, RetrievalConfidenceOut, RetrievalOut (+8 more)

### Community 1 - "Community 1"
Cohesion: 0.24
Nodes (4): Exception, AppliedCorrection, CorrectionsRepository, DuplicateActiveCorrectionError

### Community 2 - "Community 2"
Cohesion: 0.29
Nodes (12): aggregate(), _as_number_or_none(), build_call_url(), compare_to_baseline(), EvalRow, fetch_json(), load_queries(), main() (+4 more)

### Community 3 - "Community 3"
Cohesion: 0.26
Nodes (2): EmbeddedPhrase, # TODO: this function may change, and use the class properties instead of receiv

### Community 4 - "Community 4"
Cohesion: 0.21
Nodes (3): OpenAIEmbedder, _debug_enabled(), GeneratorV2

### Community 5 - "Community 5"
Cohesion: 0.36
Nodes (2): _env(), GenericPostgresql

### Community 6 - "Community 6"
Cohesion: 0.32
Nodes (2): _env(), PostgreSqlConnector

### Community 7 - "Community 7"
Cohesion: 0.50
Nodes (7): _empty_retrieval(), get_response(), _load_attribute_min_similarity(), _normalize_filters(), _normalize_response_block(), _to_int(), _to_number_or_none()

### Community 8 - "Community 8"
Cohesion: 0.38
Nodes (2): GenericPostgresql, SearchEventRepository

### Community 10 - "Community 10"
Cohesion: 0.60
Nodes (3): export_csv(), _parse_iso_dt(), summary()

### Community 12 - "Community 12"
Cohesion: 0.50
Nodes (1): V1

## Knowledge Gaps
- **Thin community `Community 3`** (2 nodes): `EmbeddedPhrase`, `# TODO: this function may change, and use the class properties instead of receiv`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 5`** (2 nodes): `_env()`, `GenericPostgresql`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 6`** (2 nodes): `_env()`, `PostgreSqlConnector`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 8`** (2 nodes): `GenericPostgresql`, `SearchEventRepository`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 12`** (1 nodes): `V1`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `GenericPostgresql` connect `Community 5` to `Community 1`, `Community 3`, `Community 6`, `Community 8`?**
  _High betweenness centrality (0.153) - this node is a cross-community bridge._
- **Why does `EmbeddedPhrase` connect `Community 3` to `Community 8`, `Community 5`, `Community 4`?**
  _High betweenness centrality (0.109) - this node is a cross-community bridge._
- **Why does `GeneratorV2` connect `Community 4` to `Community 3`?**
  _High betweenness centrality (0.064) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `EmbeddedPhrase` (e.g. with `GenericPostgresql` and `GeneratorV2`) actually correct?**
  _`EmbeddedPhrase` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `GenericPostgresql` (e.g. with `AppliedCorrection` and `CorrectionsRepository`) actually correct?**
  _`GenericPostgresql` has 7 INFERRED edges - model-reasoned connections that need verification._