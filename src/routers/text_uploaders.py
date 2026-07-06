from fastapi import Body, Path, Query, HTTPException, APIRouter
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, FileResponse, PlainTextResponse
from typing import List
from src.models.embedded_phrase_base import EmbeddedPhraseUploadBase
from src.models.embedded_phrase import EmbeddedPhrase
from src.response_api.openai_embedder import OpenAIEmbedder
from src.response_api.text_generation.v1 import V1 as TextConsult
from src.response_api.text_generation.v2 import GeneratorV2
text_uploader = APIRouter()


@text_uploader.post('/phrase', tags=['Uploaders'])
def upload_phrase(embedded_phrase_data: EmbeddedPhraseUploadBase) -> bool:
    print(embedded_phrase_data)
    attribute_code = embedded_phrase_data.attribute_code
    attribute_value_string = embedded_phrase_data.attribute_value_string
    attribute_value_number = embedded_phrase_data.attribute_value_number
    phrase = embedded_phrase_data.phrase

    obj = EmbeddedPhrase(
        attribute_code=attribute_code,
        attribute_value_string=attribute_value_string,
        attribute_value_number=attribute_value_number,
        phrase=phrase
    )
    open_ai_embedder = OpenAIEmbedder()
    api_result = open_ai_embedder.get_embedding(phrase)
    print(api_result)
    # api_result = open_ai_embedder.get_embedding("hola mundo")
    text_used = api_result['texts']
    embedding_array = api_result['embeddings'][0].tolist()
    print(text_used, ' |||||| ', embedding_array)

    insertion_result = obj.insert_row(
        attribute_code=attribute_code,
        phrase=phrase,
        embedding=embedding_array,
        attribute_value_string=attribute_value_string,
        attribute_value_number=attribute_value_number
    )
    return insertion_result


@text_uploader.get('/get_response', tags=['Uploaders'])
def get_response(user_query: str):
    consult_class = TextConsult()
    return consult_class.extract_search_intent(user_query=user_query)


@text_uploader.get('/get_responsev2', tags=['Uploaders'])
def get_response(user_query: str):
    consult_class = GeneratorV2()
    return consult_class.extract_search_intent(user_query=user_query)
