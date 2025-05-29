import os
from app.utils.query_parser import parse_query

def run(connector):
    try:
        query = parse_query(
            os.path.join(os.path.dirname(__file__), 'sql', 'get_users.sql'),
        )
        response = connector.run_query(query)
        return [name for (name,) in response]
    except Exception as e:
        print("Failed to get users:", e)
        return []