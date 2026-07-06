import os


def get_openai_key() -> str:
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError(
            "OPENAI_API_KEY no está en .env ni en variables de entorno")
    return key
