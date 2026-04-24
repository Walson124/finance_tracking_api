def run(connector, data):
    try:
        sql = """
            SELECT name, goal_amount, current_progress, monthly_contribution,
                   target_month, target_year
            FROM financial.goals
            ORDER BY created_at
        """
        rows = connector.run_query(sql)
        goal_data = [
            {
                "name": row[0],
                "goal": float(row[1]),
                "progress": float(row[2]),
                "monthly": float(row[3]),
                "target_month": row[4],
                "target_year": row[5],
            }
            for row in (rows or [])
        ]
        return {"goal_data": goal_data}
    except Exception as e:
        print(f"Error in goals get_data_service: {e}")
        return {"goal_data": []}
