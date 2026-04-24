def run(connector, data):
    try:
        month = data.get('month')
        year = data.get('year')
        sql = """
            SELECT name, amount, category, assigned_user
            FROM financial.bills
            WHERE month = %s AND year = %s
        """
        result = connector.run_query(sql, (month, year))
        if result is None:
            return []
        return [dict(zip(['name', 'amount', 'category', 'assigned_user'], tup)) for tup in result]
    except Exception as e:
        print("An error occurred in get_data_service.py:", e)
        return []