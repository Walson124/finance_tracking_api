import os
from app.utils.query_parser import parse_query

def get_data(connector):
    try:
        query = parse_query(
            os.path.join(os.path.dirname(__file__), 'sql', 'get_data.sql'),
        )
        result = connector.run_query(query)
        result = [{'year': r[0], 'month': r[1], 'category': r[2], 'sum': r[3]} for r in result]
        return result
    except Exception as e:
        print(e)
    return []