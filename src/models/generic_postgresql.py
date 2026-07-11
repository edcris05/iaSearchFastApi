from src.dbpersistence.postgresql.connector import PostgreSqlConnector
from pathlib import Path
from dotenv import load_dotenv
import os
import psycopg


def _load_project_env() -> None:
    env_path = Path(__file__).resolve().parents[2] / ".env"
    load_dotenv(dotenv_path=env_path, override=False)


def _env(name: str, default: str | None = None) -> str | None:
    value = os.getenv(name, default)
    if value is None:
        return None
    return str(value).strip().strip('"').strip("'")


_load_project_env()


class GenericPostgresql:
    def __init__(self):
        password = _env("PSQL_DB_PASSWORD") or _env("PSQL_PASSWORD")
        self.connection = psycopg.connect(
            host=_env("PSQL_HOST"),
            port=_env("PSQL_PORT"),
            dbname=_env("PSQL_DBNAME"),
            user=_env("PSQL_DB_USER"),
            password=password,
        )

    def get_connection(self):
        postgre_sql = PostgreSqlConnector()
        return postgre_sql.get_connection()

    # data es tupla
    def insert_single_row(self, sql_query, data) -> bool:
        conn = self.get_connection()
        result = False
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql_query, data)
                conn.commit()
                result = True
        except Exception as e:
            conn.rollback()  # Revertir si hay error
            raise e
        finally:
            conn.close()  # ¡INDISPENSABLE! Liberar el recurso
        return result

    def execute_select(self, sql_query, data):
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql_query, data)
                return cursor.fetchall()
        finally:
            conn.close()
