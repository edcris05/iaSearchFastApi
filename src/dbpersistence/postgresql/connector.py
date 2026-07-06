from dotenv import load_dotenv
import os
import psycopg

load_dotenv()


class PostgreSqlConnector:
    def __init__(self):
        self.connection = psycopg.connect(
            host=os.getenv("PSQL_HOST"),
            port=os.getenv("PSQL_PORT"),
            dbname=os.getenv("PSQL_DBNAME"),
            user=os.getenv("PSQL_DB_USER"),
            password=os.getenv("PSQL_DB_PASSWORD"),
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
