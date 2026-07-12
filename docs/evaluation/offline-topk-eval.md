# Offline Eval: top_k 1 vs 3

This evaluation package compares retrieval behavior across `top_k` values for FastAPI `GET /get_response/v1`.

## Files

- `scripts/eval_topk.py`: evaluator script
- `scripts/eval_queries_sample.csv`: sample query set (editable)
- output folder: `var/evaluation/<run_id>/`

## What it measures

Per `top_k`:

- response success/error counts
- source distribution (`semantic`, `fallback`, `ia`)
- fallback reasons
- filter hit rate (`has_filters_rate`)
- average and p95 latency
- average top similarity and margin
- average selected rerank score

Against baseline (first top_k in `--topk-values`, usually `1`):

- selected candidate changed rate
- queries that became `semantic`
- queries that became `fallback`

## Run

From repo root:

```bash
python3 scripts/eval_topk.py \
  --endpoint "http://localhost:8010/get_response/v1" \
  --dataset "scripts/eval_queries_sample.csv" \
  --platform magento \
  --tenant-id base \
  --locale es_AR \
  --store-code default \
  --min-similarity 0.30 \
  --topk-values "1,3"
```

Optional quick run:

```bash
python3 scripts/eval_topk.py --topk-values "1,3" --limit 5
```

## Outputs

- `summary.json`: aggregate metrics and baseline comparison
- `raw_results.csv`: per-query detail for analysis and debugging

## Decision criteria (recommended)

Promote `top_k=3` in production if all conditions hold:

- no material latency regression (e.g. p95 increase <= 20%)
- no increase in fallback rate
- equal or better semantic coverage
- meaningful candidate improvements (changed selections) in relevant queries

If latency cost is high with minimal quality gain, keep `top_k=1`.
