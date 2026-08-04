import os
import unittest

from src.utils.scope_config import resolve_scoped_env, scoped_env_names


class ScopeConfigTests(unittest.TestCase):
    def setUp(self):
        self.env_backup = dict(os.environ)

    def tearDown(self):
        os.environ.clear()
        os.environ.update(self.env_backup)

    def test_scoped_env_names_build_expected_hierarchy(self):
        names = scoped_env_names(
            base="INTENT_SYSTEM_PROMPT",
            platform="shopify",
            tenant_id="tenant-a",
            locale="es_AR",
            store_code="tienda-1",
        )
        self.assertEqual(
            names,
            [
                "INTENT_SYSTEM_PROMPT__SHOPIFY",
                "INTENT_SYSTEM_PROMPT__SHOPIFY__TENANT_A",
                "INTENT_SYSTEM_PROMPT__SHOPIFY__TENANT_A__ES_AR",
                "INTENT_SYSTEM_PROMPT__SHOPIFY__TENANT_A__ES_AR__TIENDA_1",
            ],
        )

    def test_resolve_scoped_env_prefers_most_specific_override(self):
        os.environ["INTENT_SYSTEM_PROMPT"] = "global"
        os.environ["INTENT_SYSTEM_PROMPT__ECOMMERCE"] = "platform"
        os.environ["INTENT_SYSTEM_PROMPT__ECOMMERCE__DEFAULT"] = "tenant"
        os.environ["INTENT_SYSTEM_PROMPT__ECOMMERCE__DEFAULT__ES"] = "locale"
        os.environ["INTENT_SYSTEM_PROMPT__ECOMMERCE__DEFAULT__ES__MAIN"] = "store"

        resolved = resolve_scoped_env(
            base="INTENT_SYSTEM_PROMPT",
            platform="ecommerce",
            tenant_id="default",
            locale="es",
            store_code="main",
            default="fallback",
        )

        self.assertEqual(resolved, "store")


if __name__ == "__main__":
    unittest.main()
