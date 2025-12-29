def safe_div(a, b, default=0.0):
    return (a / b) if b else default


def sum_last_n(arr, n):
    return float(sum(arr[-n:])) if arr else 0.0


def avg_last_n(arr, n):
    if not arr:
        return 0.0
    n = min(n, len(arr))
    return float(sum(arr[-n:]) / n) if n else 0.0


def run(connector, data):
    last12 = data.get("last12", [])
    pairs = [(item["fullMonth"], item["year"]) for item in last12]

    # ---------- SPENT (bills) ----------
    spent_totals = {(m, y): 0.0 for (m, y) in pairs}

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
                    spent_totals[(month, year)] = float(total or 0)

    spent_results = [spent_totals[(item["fullMonth"], item["year"])] for item in last12]
    if not spent_results:
        spent_results = [0.0] * len(last12)

    # ---------- INCOME (COMBINED across all people) ----------
    income_totals = {(m, y): 0.0 for (m, y) in pairs}

    if pairs:
        values_sql = ",".join(["(%s,%s)"] * len(pairs))
        params = []
        for m, y in pairs:
            params.extend([m, y])

        sql = f"""
            SELECT month, year, COALESCE(SUM(income), 0) AS total
            FROM financial.income
            WHERE (month, year) IN ({values_sql})
            GROUP BY month, year
        """

        with connector.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                for month, year, total in cur.fetchall():
                    income_totals[(month, year)] = float(total or 0)

    income_results = [
        income_totals[(item["fullMonth"], item["year"])] for item in last12
    ]
    if not income_results:
        income_results = [0.0] * len(last12)

    # ---------- Derived ----------
    labels = [f"{item['fullMonth']} {item['year']}" for item in last12]
    net_results = [float(i - s) for i, s in zip(income_results, spent_results)]

    last_income = float(income_results[-1]) if income_results else 0.0
    last_spent = float(spent_results[-1]) if spent_results else 0.0
    last_net = float(net_results[-1]) if net_results else 0.0

    prev_income = float(income_results[-2]) if len(income_results) >= 2 else 0.0
    prev_spent = float(spent_results[-2]) if len(spent_results) >= 2 else 0.0
    prev_net = float(net_results[-2]) if len(net_results) >= 2 else 0.0

    income_mom_delta = last_income - prev_income
    spent_mom_delta = last_spent - prev_spent
    net_mom_delta = last_net - prev_net

    income_mom_pct = safe_div(income_mom_delta, prev_income, 0.0)
    spent_mom_pct = safe_div(spent_mom_delta, prev_spent, 0.0)
    net_mom_pct = safe_div(net_mom_delta, abs(prev_net), 0.0)  # net can be negative

    widgets = {
        # current
        "income_last_month": last_income,
        "spent_last_month": last_spent,
        "net_last_month": last_net,
        # totals (window)
        "income_total_12m": float(sum(income_results)),
        "spent_total_12m": float(sum(spent_results)),
        "net_total_12m": float(sum(net_results)),
        # averages
        "income_avg_3m": avg_last_n(income_results, 3),
        "spent_avg_3m": avg_last_n(spent_results, 3),
        "net_avg_3m": avg_last_n(net_results, 3),
        # rates
        "savings_rate_last_month": safe_div(last_net, last_income, 0.0),  # net / income
        "burn_rate_last_month": safe_div(
            last_spent, last_income, 0.0
        ),  # spent / income
        "savings_rate_3m": safe_div(
            sum_last_n(net_results, 3), sum_last_n(income_results, 3), 0.0
        ),
        "burn_rate_3m": safe_div(
            sum_last_n(spent_results, 3), sum_last_n(income_results, 3), 0.0
        ),
        # deltas
        "income_mom_delta": income_mom_delta,
        "spent_mom_delta": spent_mom_delta,
        "net_mom_delta": net_mom_delta,
        "income_mom_pct": income_mom_pct,
        "spent_mom_pct": spent_mom_pct,
        "net_mom_pct": net_mom_pct,
    }

    cashflow = {
        "labels": labels,
        "income": income_results,  # combined
        "spent": spent_results,
        "net": net_results,
    }

    return {"widgets": widgets, "cashflow": cashflow, "recents": {}}
