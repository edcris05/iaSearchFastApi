import os

import httpx
import numpy as np
from openai import OpenAI

from src.utils import get_openai_key

# to avoid truncate of numpy results
np.set_printoptions(threshold=np.inf)

# class OpenAIEmbedder:
#     def __init__(self):
#         load_dotenv()
#         openai.api_key = os.getenv('OPENAI_API_KEY')

#     def get_embedding(self, texts):
#         resp = openai.embeddings.create(
#             model="text-embedding-3-small",
#             input=texts
#         )
#         return [np.array(d.embedding, dtype=np.float32) for d in resp.data]


class OpenAIEmbedder:
    def __init__(self, model: str = "text-embedding-3-small"):
        # def __init__(self, model: str = "text-embedding-3-large"):

        api_key = get_openai_key()

        # En este entorno el TLS está interceptado por Zscaler (MITM).
        # Usamos el Root CA exportado, o uno custom si se define CUSTOM_CA_BUNDLE.
        ca_bundle_path = os.getenv("CUSTOM_CA_BUNDLE", "certs/Zscaler_Root_CA.pem")
        http_client = httpx.Client(verify=ca_bundle_path)

        self.client = OpenAI(api_key=api_key, http_client=http_client)
        self.model = model

    def get_embedding(self, texts: list[str]) -> dict[str, any]:
        response = self.client.embeddings.create(
            model=self.model,
            input=texts
        )

        embeddings = [np.array(item.embedding, dtype=np.float32)
                      for item in response.data]

        return {
            "texts": texts,
            "embeddings": embeddings,
            "model": response.model,
            "usage": response.usage.model_dump(),
            # "raw_response": response
        }

    def __repr__(self):
        return f"<OpenAiEmbedder model='{self.model}'>"
