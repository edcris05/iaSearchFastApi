from src.dbpersistence.postgresql.connector import PostgreSqlConnector
import os
import psycopg


class GenericPostgresql:
    def __init__(self):
        self.connection = psycopg.connect(
            host=os.getenv("PSQL_HOST"),
            port=os.getenv("PSQL_PORT"),
            dbname=os.getenv("PSQL_DBNAME"),
            user=os.getenv("PSQL_DB_USER"),
            password=os.getenv("PSQL_DB_PASSWORD"),
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
