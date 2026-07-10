-- 002_embedded_phrase_multitenant.sql
-- Goal: scope semantic phrase embeddings by platform/tenant/store locale.

ALTER TABLE embedded_phrase
    ADD COLUMN IF NOT EXISTS platform text,
    ADD COLUMN IF NOT EXISTS tenant_id text,
    ADD COLUMN IF NOT EXISTS locale text,
    ADD COLUMN IF NOT EXISTS store_code text;

UPDATE embedded_phrase
SET platform = COALESCE(NULLIF(platform, ''), 'magento'),
    tenant_id = COALESCE(NULLIF(tenant_id, ''), 'default'),
    locale = COALESCE(NULLIF(locale, ''), 'es_AR'),
    store_code = COALESCE(NULLIF(store_code, ''), 'default')
WHERE platform IS NULL
   OR tenant_id IS NULL
   OR locale IS NULL
   OR store_code IS NULL
   OR platform = ''
   OR tenant_id = ''
   OR locale = ''
   OR store_code = '';

ALTER TABLE embedded_phrase
    ALTER COLUMN platform SET NOT NULL,
    ALTER COLUMN tenant_id SET NOT NULL,
    ALTER COLUMN locale SET NOT NULL,
    ALTER COLUMN store_code SET NOT NULL;

ALTER TABLE embedded_phrase
    ALTER COLUMN platform SET DEFAULT 'magento',
    ALTER COLUMN tenant_id SET DEFAULT 'default',
    ALTER COLUMN locale SET DEFAULT 'es_AR',
    ALTER COLUMN store_code SET DEFAULT 'default';

CREATE INDEX IF NOT EXISTS idx_embedded_phrase_scope
ON embedded_phrase (platform, tenant_id, locale, store_code, attribute_code);

-- Keep your existing vector index on embedding. The query path becomes:
-- 1) scope by platform/tenant/locale/store_code
-- 2) rank nearest vectors within that slice