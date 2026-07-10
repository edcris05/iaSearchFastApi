-- 003_embedded_phrase_backfill_movistar_base.sql
-- Goal: move legacy embedded_phrase rows from default/default scope
-- into the real Magento scope currently used by queries.
--
-- Current runtime scope observed in requests:
--   platform   = 'magento'
--   tenant_id  = 'base'
--   locale     = 'es_AR'
--   store_code = 'default'

-- 1) Inspect current distribution before changing data.
SELECT platform, tenant_id, locale, store_code, COUNT(*) AS total_rows
FROM embedded_phrase
GROUP BY platform, tenant_id, locale, store_code
ORDER BY total_rows DESC, platform, tenant_id, locale, store_code;

-- 2) Backfill legacy rows that were migrated as default/default.
UPDATE embedded_phrase
SET tenant_id = 'base',
    locale = 'es_AR',
    store_code = 'default'
WHERE platform = 'magento'
  AND tenant_id = 'default'
  AND store_code = 'default';

-- 3) Verify the result.
SELECT platform, tenant_id, locale, store_code, COUNT(*) AS total_rows
FROM embedded_phrase
GROUP BY platform, tenant_id, locale, store_code
ORDER BY total_rows DESC, platform, tenant_id, locale, store_code;

-- 4) Optional: inspect color rows after backfill.
SELECT id, platform, tenant_id, locale, store_code, attribute_code, attribute_value_number, phrase
FROM embedded_phrase
WHERE attribute_code = 'color'
ORDER BY id;