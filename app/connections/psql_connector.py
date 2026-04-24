import os
from contextlib import contextmanager

import psycopg2
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import execute_values


class psql_connector:
    def __init__(self):
        self._pool = ThreadedConnectionPool(
            minconn=0,
            maxconn=10,
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host='postgres',
            port=5432,
        )

    @contextmanager
    def connect(self):
        conn = self._pool.getconn()
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            self._pool.putconn(conn)

    def run_query(self, query, params=None):
        with self.connect() as conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute(query, params)
                    if query.strip().upper().startswith("SELECT"):
                        return cursor.fetchall()
                    return cursor.rowcount
            except Exception as e:
                print(f"Error executing query: {e}")
                raise

    def run_bulk_insert_values(self, query, values, page_size=1000):
        with self.connect() as conn:
            try:
                with conn.cursor() as cursor:
                    execute_values(cursor, query, values, page_size=page_size)
                    return cursor.rowcount
            except Exception as e:
                print(f"Error executing bulk insert: {e}")
                raise
