-- 001_corrections_active_uniqueness.sql
-- Goal: prevent duplicate ACTIVE corrections for the same logical key.
-- Logical key: platform + tenant_id + locale + attribute_code + normalized(raw_phrase)
-- normalized(raw_phrase) = lower(trim(raw_phrase))

-- 1) Inspect duplicates before adding the unique partial index.
SELECT
    platform,
    tenant_id,
    locale,
    attribute_code,
    lower(btrim(raw_phrase)) AS raw_phrase_norm,
    COUNT(*) AS active_duplicates,
    array_agg(id ORDER BY id) AS correction_ids
FROM corrections
WHERE is_active = true
GROUP BY platform, tenant_id, locale, attribute_code, lower(btrim(raw_phrase))
HAVING COUNT(*) > 1
ORDER BY active_duplicates DESC, platform, tenant_id, locale, attribute_code;

-- 2) Optional cleanup strategy (safe soft-deactivation):
-- Keep the smallest id in each duplicate group active; deactivate the rest.
-- Run this only if the previous query returns rows.
--
-- WITH ranked AS (
--     SELECT
--         id,
--         ROW_NUMBER() OVER (
--             PARTITION BY platform, tenant_id, locale, attribute_code, lower(btrim(raw_phrase))
--             ORDER BY id ASC
--         ) AS rn
--     FROM corrections
--     WHERE is_active = true
-- )
-- UPDATE corrections c
-- SET is_active = false,
--     updated_at = now()
-- FROM ranked r
-- WHERE c.id = r.id
--   AND r.rn > 1;

-- 3) Enforce uniqueness at DB level.
CREATE UNIQUE INDEX IF NOT EXISTS ux_corrections_active_logical_key
ON corrections (platform, tenant_id, locale, attribute_code, (lower(btrim(raw_phrase))))
WHERE is_active = true;
