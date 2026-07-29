from fastapi import FastAPI
from dotenv import load_dotenv
from src.dbpersistence.postgresql import PostgreSqlConnector
from src.routers.text_uploaders import text_uploader
from src.routers.user_queries import user_queries_router
from src.routers.corrections import corrections_router
from src.routers.metrics import metrics_router
from src.routers.chat_turn import chat_turn_router

app = FastAPI()

load_dotenv()


@app.get('/')
def home():
    a = PostgreSqlConnector()
    con = a.get_connection()
    print(con)
    print(con.__str__())
    return con.__str__()


app.include_router(prefix='/uploader', router=text_uploader)
app.include_router(prefix='/get_response', router=user_queries_router)
app.include_router(prefix='/corrections', router=corrections_router)
app.include_router(prefix='/metrics', router=metrics_router)
app.include_router(prefix='/chat_turn', router=chat_turn_router)
