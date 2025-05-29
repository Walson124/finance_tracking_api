import os

from app.utils.query_parser import parse_query

def run(connector, data):
    try:
        query = parse_query(
            os.path.join(os.path.dirname(__file__), 'sql', 'get_rows.sql'),
            month=data.get('month'),
            year=data.get('year'),
        )
        result = connector.run_query(
            query
        )
        print('Result from get_data_service:', result)
        if result is None:
            print("No data found or query execution failed.")
            return []
        result = [dict(zip(['name', 'amount', 'category', 'assigned_user'], tup)) for tup in result]
        return result
    except Exception as e:
        print("An error occurred in get_data_service.py:", e)
        return []