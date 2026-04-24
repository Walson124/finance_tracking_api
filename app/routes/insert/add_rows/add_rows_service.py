# import os

# from app.utils.query_parser import parse_query

# def run(connector, data):
#     try:
#         rows = data.get('rows', [])
        
#         # remove existing rows for the specified month and year
#         delete_query = parse_query(
#             os.path.join(os.path.dirname(__file__), 'sql', 'delete_rows.sql'),
#             month=data.get('month'),
#             year=data.get('year'),
#         )
        
#         result = connector.run_query(delete_query)
#         print('delete_query result:', result)
    
#         if len(rows) > 0:
#             conditions = []
#             for item in rows:
#                 conditions.append(f"('{item.get('name')}', {item.get('amount')}, '{item.get('category')}', '{item.get('month')}', {item.get('year')}, '{item.get('user')}')")
#             conditions_str = ', '.join(conditions)
#             # add new rows
#             add_query = parse_query(
#                 os.path.join(os.path.dirname(__file__), 'sql', 'insert_rows.sql'),
#                 conditions=conditions_str
#             )
            
#             result = connector.run_query(add_query)
#             print('add_query result:', result)
        
#         return 'success'
#     except Exception as e:
#         print("An error occurred in add_rows_service.py:", e)
#         return {"error": str(e)}

def run(connector, data):
    try:
        rows = data.get("rows", [])
        month = data.get("month")
        year = data.get("year")

        connector.run_query(
            "DELETE FROM financial.bills WHERE month = %s AND year = %s",
            (month, year),
        )

        if rows:
            values = [
                (
                    item.get("name"),
                    item.get("amount"),
                    item.get("category"),
                    item.get("month"),
                    item.get("year"),
                    item.get("user"),
                )
                for item in rows
            ]
            connector.run_bulk_insert_values(
                "INSERT INTO financial.bills (name, amount, category, month, year, assigned_user) VALUES %s",
                values,
                page_size=1000,
            )

        return "success"
    except Exception as e:
        print("An error occurred in add_rows_service.py:", e)
        return {"error": str(e)}
