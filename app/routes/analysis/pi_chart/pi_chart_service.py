def get_params(connector):
    try:
        sql = """
            SELECT DISTINCT category, year, month, name
            FROM financial.bills
        """
        result = connector.run_query(sql)
        distinct_params = {'category': set(), 'year': set(), 'month': set(), 'name': set()}
        for row in result:
            distinct_params['category'].add(row[0])
            distinct_params['year'].add(row[1])
            distinct_params['month'].add(row[2])
            distinct_params['name'].add(row[3])
        return {k: list(v) for k, v in distinct_params.items()}
    except Exception as e:
        print(f"Error fetching parameters: {e}")
        return {'category': [], 'year': [], 'month': [], 'name': []}

def get_data(connector, data):
    month = data.get('month', '')
    year = data.get('year', '')
    assigned_user = data.get('assigned_user', '')
    category = data.get('category', '')

    columns = ['name', 'amount', 'category', 'assigned_user', 'month', 'year']
    where_clauses = []
    params = []

    if month:
        where_clauses.append("month = %s")
        params.append(month)
        columns.remove('month')
    if year:
        where_clauses.append("year = %s")
        params.append(year)
        columns.remove('year')
    if assigned_user:
        where_clauses.append("assigned_user = %s")
        params.append(assigned_user)
        columns.remove('assigned_user')
    if category:
        where_clauses.append("category = %s")
        params.append(category)
        columns.remove('category')

    if not where_clauses:
        return []

    column_str = ', '.join(columns)
    where_str = ' AND '.join(where_clauses)
    sql = f"SELECT {column_str} FROM financial.bills WHERE {where_str}"

    try:
        result = connector.run_query(sql, tuple(params))
        result = [dict(zip(columns, tup)) for tup in result]

        grouped_by_result = {}
        for column in columns:
            if column != 'amount':
                temp = {}
                for row in result:
                    key = row[column]
                    if isinstance(key, str):
                        key = key.lower()
                    temp[key] = temp.get(key, 0) + row['amount']
                sorted_temp = sorted(temp.items(), key=lambda x: x[1])
                grouped_by_result[column] = [
                    {'id': i + 1, 'value': round(v, 2), 'label': k}
                    for i, (k, v) in enumerate(sorted_temp)
                ]
        return grouped_by_result
    except Exception as e:
        print(f"Error fetching data: {e}")
    return []