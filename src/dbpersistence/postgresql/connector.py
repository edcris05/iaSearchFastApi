from pathlib import Path

from dotenv import load_dotenv
import os
import psycopg


def _load_project_env() -> None:
    # Resolve .env from repository root even when process cwd differs.
    env_path = Path(__file__).resolve().parents[3] / ".env"
    load_dotenv(dotenv_path=env_path, override=False)


def _env(name: str, default: str | None = None) -> str | None:
    value = os.getenv(name, default)
    if value is None:
        return None
    return str(value).strip().strip('"').strip("'")


_load_project_env()


class PostgreSqlConnector:
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
        cursor = self.connection
        return cursor

    def close_connection(self):
        self.connection.close()

 # data es tupla
    def insert_single_row(self, sql_query, data):
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
