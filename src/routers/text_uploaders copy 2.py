import csv
import io
from fastapi import Body, Path, Query, HTTPException, APIRouter, UploadFile, File
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
 
 
@text_uploader.post("/upload-csv", tags=['Uploaders'])
async def upload_csv(file: UploadFile = File(...)):
    # Validar extensión
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="El archivo debe ser .csv")
 
    # Leer contenido
    content = await file.read()
 
    # Convertir bytes a texto
    csv_text = content.decode("utf-8")
 
    # Crear lector CSV
    csv_reader = csv.DictReader(io.StringIO(csv_text))
 
    open_ai_embedder = OpenAIEmbedder()
    # for row in csv_reader:
 
    #     print(row)
    #     print(row['attribute_code'])
 
    # Convertir filas a lista
    rows = [row for row in csv_reader]
    # print(rows)
    # insert into BD
    for row in rows:
        print(row)
        attribute_code = row['attribute_code']
        attribute_value_string = row['attribute_value_string']
        attribute_value_number = row['attribute_value_number']
        phrase = row['phrase']
        api_result = open_ai_embedder.get_embedding(phrase)
        embedding_array = api_result['embeddings'][0].tolist()
        # print(api_result)
        print(embedding_array)
        print('\n')
        print('\n')
 
        obj = EmbeddedPhrase(
            attribute_code=attribute_code,
            attribute_value_string=attribute_value_string,
            attribute_value_number=attribute_value_number,
            phrase=embedding_array
        )
 
        insertion_result = obj.insert_row(
            attribute_code=attribute_code,
            phrase=phrase,
            embedding=embedding_array,
            attribute_value_string=attribute_value_string,
            attribute_value_number=attribute_value_number
        )
    # for a in rows:
    #     # api_result = open_ai_embedder.get_embedding(a['phrase'])
    #     # text_used = api_result['texts']
    #     # embedding_array = api_result['embeddings'][0].tolist()
 
    #     attribute_code = a['attribute_code'],
    #     attribute_value_string = a['attribute_value_string'],
    #     attribute_value_number = a['attribute_value_number'],
    #     phrase = a['phrase']
 
    #     print(a)
    #     # print('\n')
    #     # print(attribute_code)
    #     # print('\n')
    #     # print(attribute_value_string)
    #     # print('\n')
    #     # print(attribute_value_number)
    #     # print('\n')
    #     # print(phrase)
    #     # print('\n')
 
    #     # obj = EmbeddedPhrase(
    #     #     attribute_code=attribute_code,
    #     #     attribute_value_string=attribute_value_string,
    #     #     attribute_value_number=attribute_value_number,
    #     #     phrase=phrase
    #     # )
    #     # insertion_result = obj.insert_row(
    #     #     attribute_code=attribute_code,
    #     #     phrase=phrase,
    #     #     embedding=embedding_array,
    #     #     attribute_value_string=attribute_value_string,
    #     #     attribute_value_number=attribute_value_number
    #     # )
    #     # print(insertion_result)
 
    return {
        "filename": file.filename,
        "total_rows": len(rows),
        "data": rows
    }