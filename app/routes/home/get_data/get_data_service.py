import random


def run(connector, data):
    last12 = data.get("last12", [])
    pairs = [(item["fullMonth"], item["year"]) for item in last12]
    totals = {(m, y): 0.0 for (m, y) in pairs}

    if pairs:
        values_sql = ",".join(["(%s,%s)"] * len(pairs))  # (month, year)
        params = []
        for m, y in pairs:
            params.extend([m, y])

        sql = f"""
            SELECT month, year, COALESCE(SUM(amount), 0) AS total
            FROM financial.bills
            WHERE (month, year) IN ({values_sql})
            GROUP BY month, year
        """

        with connector.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                for month, year, total in cur.fetchall():
                    totals[(month, year)] = float(total)

    results = [totals[(item["fullMonth"], item["year"])] for item in last12]
    if not results:
        results = [0.0] * len(last12)

    widgets = {
        "safe_to_spend": 123.45,
        "income": 1234.56,
        "spent": 888.88,
        "bills_due": 3,
    }
    cashflow = {
        "income": [8000 for i in range(12)],
        "spent": results,
    }
    return {
        "widgets": widgets,
        "cashflow": cashflow,
        "recents": {},
    }
