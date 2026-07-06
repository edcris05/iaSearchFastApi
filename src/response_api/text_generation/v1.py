import json
import os
from textwrap import dedent

from openai import OpenAI


class V1:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def extract_search_intent(self, user_query: str) -> dict:
        response = self.client.responses.create(
            model="gpt-4o-mini",
            input=[
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "input_text",
                            "text": (
                                "Eres un extractor de intención para un buscador de productos. "
                                "No respondes al usuario. "
                                "No explicas nada. "
                                "Solo conviertes texto libre en filtros estructurados."
                                "No interpretas atributos."
                            )
                        }
                    ]
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": dedent(f"""
                                Extrae información de búsqueda del texto del usuario.

                                Devuelve SOLO un JSON válido, sin texto adicional, con este esquema:

                                {{
                                "query": string,
                                "price_min": number | null,
                                "price_max": number | null,
                                "attributes": string[]
                                }}

                                Reglas:
                                - Si el usuario dice "para arriba", "desde", "mínimo", "a partir de" úsalo como price_min
                                - Si dice "hasta", "máximo", úsalo como price_max
                                - Si el usuario dice "entre A y B". Usa "A" como price_min y "B" como price_max
                                - Si no se menciona precio, usa null
                                - En attributes incluye SOLO frases descriptivas literales del usuario
                                - No normalices ni interpretes atributos
                                - No inventes reglas
                                - No incluyas explicaciones
                                - Usa solo valores numéricos sin moneda
                                - Responde solo con JSON

                                Texto del usuario:
                                \"\"\"
                                {user_query}
                                \"\"\"
                                """
                            )
                        }
                    ]
                }
            ],
            temperature=0
        )

        return {
            "response": json.loads(response.output_text),
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
            "total_tokens": response.usage.total_tokens,
        }
