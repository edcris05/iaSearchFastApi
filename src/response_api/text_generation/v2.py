import json
import logging
import os
import re
from textwrap import dedent
from typing import List

import httpx
from openai import OpenAI

from src.models.embedded_phrase import EmbeddedPhrase
from src.response_api.openai_embedder import OpenAIEmbedder

logger = logging.getLogger(__name__)


def _debug_enabled() -> bool:
    return os.getenv("AI_SEARCH_DEBUG", "0").strip() == "1"


class GeneratorV2:
    def __init__(self):
        # En este entorno el TLS está siendo interceptado por Zscaler (MITM),
        # así que debemos confiar explícitamente en su CA/cadena.
        #
        # Nota: este archivo se genera con openssl s_client en certs/zscaler_chain.pem
        # y debe contener la CA que firma los certificados emitidos por Zscaler.
        ca_bundle_path = os.getenv("CUSTOM_CA_BUNDLE", "certs/Zscaler_Root_CA.pem")

        http_client = httpx.Client(verify=ca_bundle_path)
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            http_client=http_client,
        )

    def extract_search_intent(self, user_query: str) -> dict:
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

        PROMPT_TEMPLATE = dedent("""
            Extrae características de celulares desde una frase en español.

            1. Primero identifica cada característica mencionada.
            2. Luego intenta convertirlas a filtros cuantificables.
            3. Si no es cuantificable, colócala en "characteristics".

            Devuelve SOLO JSON válido con este formato:

            {{
            "price_min":number|null,
            "price_max":number|null,
            "min_battery_mah":number|null,
            "min_ram_gb":number|null,
            "min_storage_gb":number|null,
            "characteristics":[string]
            }}

            Reglas:

            PRECIO
            - "menos de", "máx", "max", "hasta" → price_max
            - "más de", "mín", "min", "desde", "al menos" → price_min
            - "entre X y Y" → price_min=X, price_max=Y

            RAM / STORAGE
            - reconoce: gb, giga, gigas, tb, tera, terabyte
            - TB → convertir a GB (1TB=1024GB)
            - si hay rango → usar el menor
            - si dice "mín", "al menos", etc → usar ese valor
            - para "máx" también devolver ese valor como mínimo requerido

            BATERÍA
            - detectar valores en mAh → min_battery_mah

            COLORES
            - dividir listas: "rojo o negro", "rojo, negro o azul"
            - devolver como: "color rojo"

            GENERAL
            - ignorar texto irrelevante
            - números sin unidad cerca de "ram" o "disco/almacenamiento" deben interpretarse como GB
            - si no hay valor → null
            - no inventar datos
            - no explicar nada

            Texto del usuario:
            \"\"\"
            {user_query}
            \"\"\"
            """).strip()

        response = self.client.responses.create(
            model="gpt-4o-mini",
            input=[
                {
                    "role": "system",
                    "content": [{
                        "type": "input_text",
                        "text": "Eres un extractor de filtros y características. Devuelves solo JSON."
                    }]
                },
                {
                    "role": "user",
                    "content": [{
                        "type": "input_text",
                        "text": PROMPT_TEMPLATE.format(user_query=user_query)
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
