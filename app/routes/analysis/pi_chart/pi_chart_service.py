import os
from app.utils.query_parser import parse_query

def get_params(connector):
    try:
        query = parse_query(
            os.path.join(os.path.dirname(__file__), 'sql', 'get_distinct_params.sql')
        )
        result = connector.run_query(query)
        distinct_params = {
            'category': set(),
            'year': set(),
            'month': set(),
            'name': set()
        }
        for row in result:
            distinct_params['category'].add(row[0])
            distinct_params['year'].add(row[1])
            distinct_params['month'].add(row[2])
            distinct_params['name'].add(row[3])
        return {temp_key: list(temp_value) for temp_key, temp_value in distinct_params.items()}
    except Exception as e:
        print(f"Error fetching parameters: {e}")
        return {'category': [], 'year': [], 'month': [], 'name': []}

def get_data(connector, data):
    # we want to return a series of data that can be used to create a pie chart
    # first we need to query based on the input data
    month = data.get('month', '')
    year = data.get('year', '')
    assigned_user = data.get('assigned_user', '')
    category = data.get('category', '')

    columns = ['name', 'amount', 'category', 'assigned_user', 'month', 'year']
    conditions = []
    if month:
        conditions.append(f"month = '{month}'")
        columns.remove('month')
    if year:
        conditions.append(f"year = '{year}'")
        columns.remove('year')
    if assigned_user:
        conditions.append(f"assigned_user = '{assigned_user}'")
        columns.remove('assigned_user')
    if category:
        conditions.append(f"category = '{category}'")
        columns.remove('category')
    
    if conditions:
        conditions = ' AND '.join(conditions)
        column_str = ', '.join(columns)
        try:
            query = parse_query(
                os.path.join(os.path.dirname(__file__), 'sql', 'get_data.sql'),
                columns=column_str,
                conditions=conditions
            )
            result = connector.run_query(query)
            result = [dict(zip(columns, tup)) for tup in result]
            
            # group by each column and sum the amounts
            grouped_by_result = {}
            for column in columns:
                if column != 'amount':
                    temp = {}
                    for row in result:
                        row_column_data = row[column]
                        if type(row[column]) is str:
                            row_column_data = row_column_data.lower()
                        if row_column_data not in temp:
                            temp[row_column_data] = 0
                        temp[row_column_data] += row['amount']
                    temp = sorted(temp.items(), key=lambda x: x[1])
                    temp = [{'id': index + 1, 'value': round(row[1], 2), 'label': row[0]} for index, row in enumerate(temp)]
                    grouped_by_result[column] = temp
            
            return grouped_by_result
        except Exception as e:
            print(f"Error fetching data: {e}")
    return []