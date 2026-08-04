import json
import logging
import os
import re
from pathlib import Path
from textwrap import dedent
from typing import List

import httpx
from openai import OpenAI

from src.models.embedded_phrase import EmbeddedPhrase
from src.response_api.openai_embedder import OpenAIEmbedder
from src.utils.domain_profile import resolve_domain_profile
from src.utils.scope_config import (
    DEFAULT_LOCALE,
    DEFAULT_PLATFORM,
    DEFAULT_STORE_CODE,
    DEFAULT_TENANT_ID,
    resolve_scoped_env,
)

logger = logging.getLogger(__name__)


def _debug_enabled() -> bool:
    return os.getenv("AI_SEARCH_DEBUG", "0").strip() == "1"


class GeneratorV2:
    def __init__(self):
        # Permite CA custom por entorno (corporativo/proxy), y si no existe
        # usa el bundle corporativo versionado en el repo.
        repo_root = Path(__file__).resolve().parents[3]
        bundle_candidates = [
            # 1) Overrides por entorno (si tu infra ya setea alguno, se respeta)
            os.getenv("CUSTOM_CA_BUNDLE", "").strip(),
            os.getenv("SSL_CERT_FILE", "").strip(),
            os.getenv("REQUESTS_CA_BUNDLE", "").strip(),
            # 2) Bundles versionados en el repo (priorizar Root CA)
            str(repo_root / "certs" / "Zscaler_Root_CA.pem"),
            str(repo_root / "certs" / "zscaler_certs_only.pem"),
            # NOTA: no usar zscaler_chain.pem como CA porque suele incluir texto extra
            # (salida completa de openssl s_client) y rompe la verificación.
        ]
        verify: str | bool = True
        for candidate in bundle_candidates:
            if candidate and Path(candidate).is_file():
                verify = candidate
                break

        logger.info("OpenAI TLS verify=%s", verify)
        http_client = httpx.Client(verify=verify)
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            http_client=http_client,
        )

    def _default_prompt_template(self, domain_profile: str) -> str:
        if domain_profile == "electronics":
            return dedent('''
                Extrae intención de búsqueda de productos electrónicos desde una frase del usuario.

                Devuelve SOLO JSON válido con este formato:
                {
                  "price_min": number|null,
                  "price_max": number|null,
                  "min_battery_mah": number|null,
                  "min_ram_gb": number|null,
                  "min_storage_gb": number|null,
                  "characteristics": [string],
                  "domain_filters": {}
                }

                Reglas generales:
                - No inventar datos.
                - Si no hay un valor claro, usar null.
                - Guardar en "characteristics" todo lo no cuantificable.
                - Reconocer expresiones de precio: "menos de", "hasta", "más de", "desde", "entre X y Y".
                - Para RAM/STORAGE/BATERIA completar los campos numéricos solo cuando haya evidencia explícita.
                - En electronics, mantener "domain_filters" vacío salvo que se indique un filtro numérico adicional no mapeado.

                Texto del usuario:
                """
                {user_query}
                """
                ''').strip()

        return dedent('''
            Extrae intención de búsqueda de productos desde una frase del usuario.

            Devuelve SOLO JSON válido con este formato:
            {
              "price_min": number|null,
              "price_max": number|null,
              "min_battery_mah": number|null,
              "min_ram_gb": number|null,
              "min_storage_gb": number|null,
              "characteristics": [string],
              "domain_filters": {"constraint_name": number}
            }

            Reglas generales:
            - No inventar datos.
            - Si no hay un valor claro, usar null.
            - Guardar en "characteristics" todo lo no cuantificable.
            - Reconocer expresiones de precio: "menos de", "hasta", "más de", "desde", "entre X y Y".
            - En perfil generic NO dependas de campos específicos de celulares.
            - Usa min_battery_mah/min_ram_gb/min_storage_gb solo si el usuario explícitamente habla de batería/RAM/almacenamiento.
            - Para restricciones numéricas de otros dominios, usar domain_filters con claves cortas en snake_case.

            Texto del usuario:
            """
            {user_query}
            """
            ''').strip()

    def _resolve_prompt_template(
        self,
        domain_profile: str,
        platform: str,
        tenant_id: str,
        locale: str,
        store_code: str,
    ) -> str:
        configured = resolve_scoped_env(
            base="INTENT_PROMPT_TEMPLATE",
            platform=platform,
            tenant_id=tenant_id,
            locale=locale,
            store_code=store_code,
            default="",
        )
        return configured if configured != "" else self._default_prompt_template(domain_profile)

    def _resolve_system_prompt(
        self,
        domain_profile: str,
        platform: str,
        tenant_id: str,
        locale: str,
        store_code: str,
    ) -> str:
        configured = resolve_scoped_env(
            base="INTENT_SYSTEM_PROMPT",
            platform=platform,
            tenant_id=tenant_id,
            locale=locale,
            store_code=store_code,
            default="",
        )
        if configured != "":
            return configured
        if domain_profile == "electronics":
            return "Eres un extractor de intención de búsqueda para catálogos de electrónica. Responde solo JSON válido."
        return "Eres un extractor de intención de búsqueda. Responde solo JSON válido."

    def _render_prompt(self, prompt_template: str, user_query: str) -> str:
        # Avoid str.format on JSON templates, because literal braces can trigger KeyError.
        return prompt_template.replace("{user_query}", user_query)

    def extract_search_intent(
        self,
        user_query: str,
        platform: str = DEFAULT_PLATFORM,
        tenant_id: str = DEFAULT_TENANT_ID,
        locale: str = DEFAULT_LOCALE,
        store_code: str = DEFAULT_STORE_CODE,
    ) -> dict:
        # return {
        #     "response": {
        #         "price_min": None,
        #         "price_max": 311,
        #         "min_battery_mah": None,
        #         "min_ram_gb": 7,
        #         "min_storage_gb": 100,
        #         "characteristics": [
        #             "color rojo",
        #             "color negro",
        #             "saca fotos nocturnas"
        #         ]
        #     },
        #     "input_tokens": 425,
        #     "output_tokens": 75,
        #     "total_tokens": 500
        # }

        domain_profile = resolve_domain_profile(
            platform=platform,
            tenant_id=tenant_id,
            locale=locale,
            store_code=store_code,
        )
        prompt_template = self._resolve_prompt_template(
            domain_profile=domain_profile,
            platform=platform,
            tenant_id=tenant_id,
            locale=locale,
            store_code=store_code,
        )
        system_prompt = self._resolve_system_prompt(
            domain_profile=domain_profile,
            platform=platform,
            tenant_id=tenant_id,
            locale=locale,
            store_code=store_code,
        )
        logger.info(
            "extract_search_intent scope platform=%s tenant_id=%s locale=%s store_code=%s domain_profile=%s",
            platform,
            tenant_id,
            locale,
            store_code,
            domain_profile,
        )

        response = self.client.responses.create(
            model="gpt-4o-mini",
            input=[
                {
                    "role": "system",
                    "content": [{
                        "type": "input_text",
                        "text": system_prompt
                    }]
                },
                {
                    "role": "user",
                    "content": [{
                        "type": "input_text",
                        "text": self._render_prompt(prompt_template, user_query)
                    }]
                }
            ],
            temperature=0
        )
        logger.info("extract_search_intent completed")
        if _debug_enabled():
            logger.debug("extract_search_intent raw response: %s", response)
            logger.debug("extract_search_intent output_text: %s", response.output_text)

        return {
            "response": self.clear_model_response(response.output_text),
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
            "total_tokens": response.usage.total_tokens,
        }
        # return response

    def clear_model_response(self, response_text: str) -> dict:
        cleaned = re.sub(r"^```json|```$", "",
                         response_text.strip(), flags=re.MULTILINE).strip()
        return json.loads(cleaned)

    def get_embedding_filter_by_attributes(
        self,
        attributes: List,
        query_text: str,
        platform: str,
        tenant_id: str,
        locale: str,
        store_code: str,
        min_similarity: float = 0.30,
        top_k: int = 2,
        attribute_min_similarity: dict[str, float] | None = None,
    ):
        # Si no hay characteristics, no debemos llamar embeddings (OpenAI 400: empty array).
        if not attributes:
            return []

        embedding = OpenAIEmbedder()
        embedded_phrase = EmbeddedPhrase()
        embedded_response = embedding.get_embedding(attributes)
        logger.info(
            "embedding generated texts=%s vectors=%s model=%s",
            len(embedded_response.get("texts", [])),
            len(embedded_response.get("embeddings", [])),
            embedded_response.get("model", "unknown"),
        )
        if _debug_enabled():
            logger.debug("embedded_response usage=%s", embedded_response.get("usage", {}))

        texts_used = embedded_response["texts"]
        embedded_texts = embedded_response["embeddings"]
        logger.info("selecting from postgres for %s embedded text(s)", len(texts_used))
        try:
            results = embedded_phrase.select_row_with_diagnostics(
                embeddings=embedded_texts,
                query_text=query_text,
                platform=platform,
                tenant_id=tenant_id,
                locale=locale,
                store_code=store_code,
                min_similarity=min_similarity,
                top_k=top_k,
                attribute_min_similarity=attribute_min_similarity,
            )
        except Exception:
            logger.exception("select_row_with_diagnostics failed")
            raise
        if _debug_enabled():
            logger.debug("select_row_with_diagnostics results: %s", results)
        return results
        # # busqueda:
        # celu de 500 pesos, con batería de larga duración de al menos 5000 mili amperios

        # # output
        # Response(id='resp_01adfb0d53794ca8006986e0f78da081958ec73c72a856a991', created_at=1770447095.0, error=None, incomplete_details=None, instructions=None, metadata={}, model='gpt-4o-mini-2024-07-18', object='response', output=[ResponseOutputMessage(id='msg_01adfb0d53794ca8006986e0f7d440819593349e624e79f8bb', content=[ResponseOutputText(annotations=[], text='```json\n{\n  "price_min": 500,\n  "price_max": 500,\n  "min_battery_mah": 5000,\n  "attributes": [\n    "batería de larga duración"\n  ]\n}\n```', type='output_text', logprobs=[])], role='assistant', status='completed', type='message')], parallel_tool_calls=True, temperature=0.0, tool_choice='auto', tools=[], top_p=1.0, background=False, completed_at=1770447096.0, conversation=None, max_output_tokens=None, max_tool_calls=None, previous_response_id=None, prompt=None, prompt_cache_key=None, prompt_cache_retention=None, reasoning=Reasoning(effort=None, generate_summary=None, summary=None), safety_identifier=None, service_tier='default', status='completed', text=ResponseTextConfig(format=ResponseFormatText(type='text'), verbosity='medium'), top_logprobs=0, truncation='disabled', usage=ResponseUsage(input_tokens=180, input_tokens_details=InputTokensDetails(cached_tokens=0), output_tokens=51, output_tokens_details=OutputTokensDetails(reasoning_tokens=0), total_tokens=231), user=None, billing={'payer': 'developer'}, frequency_penalty=0.0, presence_penalty=0.0, store=True)

        # {
        #   "response": {
        #     "price_min": 500,
        #     "price_max": 500,
        #     "min_battery_mah": 5000,
        #     "attributes": [
        #       "batería de larga duración"
        #     ]
        #   },
        #   "input_tokens": 180,
        #   "output_tokens": 51,
        #   "total_tokens": 231
        # }
