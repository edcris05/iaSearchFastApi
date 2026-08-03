import logging

from fastapi import FastAPI
from dotenv import load_dotenv
from src.dbpersistence.postgresql import PostgreSqlConnector
from src.routers.text_uploaders import text_uploader
from src.routers.user_queries import user_queries_router
from src.routers.corrections import corrections_router
from src.routers.metrics import metrics_router
from src.routers.chat_turn import chat_turn_router

app = FastAPI()
logger = logging.getLogger("uvicorn.error")

load_dotenv()


@app.get('/')
def home():
    a = PostgreSqlConnector()
    con = a.get_connection()
    print(con)
    print(con.__str__())
    return con.__str__()


@app.get('/_routes')
def list_routes():
    routes = []
    for route in app.routes:
        path = getattr(route, 'path', '')
        methods = sorted(list(getattr(route, 'methods', []) or []))
        if path:
            routes.append({
                'path': path,
                'methods': methods,
            })
    return {
        'count': len(routes),
        'routes': routes,
    }


app.include_router(prefix='/uploader', router=text_uploader)
app.include_router(prefix='/get_response', router=user_queries_router)
app.include_router(prefix='/corrections', router=corrections_router)
app.include_router(prefix='/metrics', router=metrics_router)
app.include_router(prefix='/chat_turn', router=chat_turn_router)

# Compatibilidad temporal mientras todos los clientes migran al endpoint dedicado.
app.include_router(prefix='/get_response/chat_turn', router=chat_turn_router)

logger.info('FastAPI routes ready', extra={'chat_routes': ['/chat_turn/', '/get_response/chat_turn/']})
