import os
import psycopg2

class psql_connector:
    def __init__(self):
        self.db_name = os.getenv('DB_NAME')
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        self.host = 'postgres'
        self.port = 5432

    def connect(self):
        try:
            connection = psycopg2.connect(
                dbname=self.db_name,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            return connection
        except Exception as e:
            print(f"Error connecting to PostgreSQL database: {e}")
            return None
        
    def run_query(self, query, params=None):
        connection = self.connect()
        if connection is None:
            return None
        
        try:
            print('Executing query:', query)
            cursor = connection.cursor()
            
            # Check if it's a SELECT query or modification query (INSERT/DELETE/UPDATE)
            if query.strip().upper().startswith("SELECT"):
                # For SELECT, fetch the results
                cursor.execute(query, params)
                result = cursor.fetchall()
                print('Query executed successfully')
                print('Result:', result)
                return result
            
            else:
                # For INSERT/DELETE/UPDATE, commit the changes but don't fetch results
                cursor.execute(query, params)
                connection.commit()
                print('Query executed successfully (INSERT/DELETE/UPDATE)')
                return cursor.rowcount  # Return the number of affected rows
        except Exception as e:
            print(f"Error executing query: {e}")
            return None
        finally:
            cursor.close()
            connection.close()
