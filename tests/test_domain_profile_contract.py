import os
import unittest

from src.utils.domain_profile import normalize_domain_profile, resolve_domain_profile
from src.utils.intent_normalization import normalize_response_block


class DomainProfileContractTests(unittest.TestCase):
    def setUp(self):
        self.env_backup = dict(os.environ)

    def tearDown(self):
        os.environ.clear()
        os.environ.update(self.env_backup)

    def test_domain_profile_scoped_override(self):
        os.environ["INTENT_DOMAIN_PROFILE"] = "generic"
        os.environ["INTENT_DOMAIN_PROFILE__ECOMMERCE__DEFAULT__ES__MAIN"] = "electronics"

        resolved = resolve_domain_profile(
            platform="ecommerce",
            tenant_id="default",
            locale="es",
            store_code="main",
        )

        self.assertEqual(resolved, "electronics")

    def test_normalize_domain_profile_fallback(self):
        self.assertEqual(normalize_domain_profile("unknown"), "generic")
        self.assertEqual(normalize_domain_profile("ELECTRONICS"), "electronics")

    def test_normalize_response_uses_aliases_and_domain_filters(self):
        payload = {
            "price_from": "100",
            "price_to": "200",
            "battery_min": "4500",
            "characteristics": ["durable", ""],
            "domain_filters": {
                "screen_inches_min": "6.1",
                "bad_value": "n/a",
            },
        }
        aliases = {
            "price_min": ["price_from"],
            "price_max": ["price_to"],
            "min_battery_mah": ["battery_min"],
        }

        out = normalize_response_block(payload, numeric_aliases=aliases)

        self.assertEqual(out["price_min"], 100)
        self.assertEqual(out["price_max"], 200)
        self.assertEqual(out["min_battery_mah"], 4500)
        self.assertEqual(out["characteristics"], ["durable"])
        self.assertEqual(out["domain_filters"], {"screen_inches_min": 6.1})

if __name__ == "__main__":
    unittest.main()
