def safe_div(a, b, default=0.0):
    try:
        return a / b if b else default
    except Exception:
        return default


def sum_last_n(arr, n):
    return float(sum(arr[-n:])) if arr else 0.0


def avg_last_n(arr, n):
    if not arr:
        return 0.0
    n = min(n, len(arr))
    return float(sum(arr[-n:]) / n) if n else 0.0


def run(connector, data):
    user = (data.get("user") or "").strip()
    last12 = data.get("last12", [])

    # ---------- SPENT (from bills) ----------
    bill_pairs = [(item["fullMonth"], item["year"]) for item in last12]
    spent_totals = {(m, y): 0.0 for (m, y) in bill_pairs}

    if bill_pairs:
        values_sql = ",".join(["(%s,%s)"] * len(bill_pairs))
        params = []
        for m, y in bill_pairs:
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

    # ---------- INCOME (from income table) ----------
    income_totals = {(m, y): 0.0 for (m, y) in bill_pairs}

    if user and bill_pairs:
        values_sql = ",".join(["(%s,%s)"] * len(bill_pairs))
        params = [user]
        for m, y in bill_pairs:
            params.extend([m, y])

        sql = f"""
            SELECT month, year, COALESCE(SUM(income), 0) AS total
            FROM financial.income
            WHERE person_nm = %s
              AND (month, year) IN ({values_sql})
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

    # ---------- Derived arrays ----------
    net_results = [
        float(i - s) for i, s in zip(income_results, spent_results)
    ]  # net cashflow per month

    # treat last element as "most recent"
    last_income = float(income_results[-1]) if income_results else 0.0
    last_spent = float(spent_results[-1]) if spent_results else 0.0
    last_net = float(net_results[-1]) if net_results else 0.0

    prev_income = float(income_results[-2]) if len(income_results) >= 2 else 0.0
    prev_spent = float(spent_results[-2]) if len(spent_results) >= 2 else 0.0
    prev_net = float(net_results[-2]) if len(net_results) >= 2 else 0.0

    income_3m_avg = avg_last_n(income_results, 3)
    spent_3m_avg = avg_last_n(spent_results, 3)
    net_3m_avg = avg_last_n(net_results, 3)

    income_12m_total = float(sum(income_results))
    spent_12m_total = float(sum(spent_results))
    net_12m_total = float(sum(net_results))

    savings_rate_last = safe_div(last_net, last_income, default=0.0)  # net / income
    savings_rate_3m = safe_div(
        sum_last_n(net_results, 3), sum_last_n(income_results, 3), default=0.0
    )
    burn_rate_last = safe_div(last_spent, last_income, default=0.0)  # spent / income
    burn_rate_3m = safe_div(
        sum_last_n(spent_results, 3), sum_last_n(income_results, 3), default=0.0
    )

    # Best/worst months in the last12 window
    best_net = max(net_results) if net_results else 0.0
    worst_net = min(net_results) if net_results else 0.0
    best_idx = net_results.index(best_net) if net_results else -1
    worst_idx = net_results.index(worst_net) if net_results else -1

    labels = [
        f"{item['fullMonth']} {item['year']}" for item in last12
    ]  # for frontend display
    best_label = labels[best_idx] if 0 <= best_idx < len(labels) else None
    worst_label = labels[worst_idx] if 0 <= worst_idx < len(labels) else None

    # MoM deltas
    income_mom_delta = last_income - prev_income
    spent_mom_delta = last_spent - prev_spent
    net_mom_delta = last_net - prev_net
    income_mom_pct = safe_div(income_mom_delta, prev_income, default=0.0)
    spent_mom_pct = safe_div(spent_mom_delta, prev_spent, default=0.0)
    net_mom_pct = safe_div(
        net_mom_delta, abs(prev_net), default=0.0
    )  # net can be negative

    # ---------- Widgets ----------
    widgets = {
        # basics
        "income_last_month": last_income,
        "spent_last_month": last_spent,
        "net_last_month": last_net,  # income - spent
        # averages
        "income_avg_3m": income_3m_avg,
        "spent_avg_3m": spent_3m_avg,
        "net_avg_3m": net_3m_avg,
        # totals in the last12 window
        "income_total_12m": income_12m_total,
        "spent_total_12m": spent_12m_total,
        "net_total_12m": net_12m_total,
        # rates
        "savings_rate_last_month": savings_rate_last,  # net / income
        "savings_rate_3m": savings_rate_3m,
        "burn_rate_last_month": burn_rate_last,  # spent / income
        "burn_rate_3m": burn_rate_3m,
        # deltas
        "income_mom_delta": income_mom_delta,
        "spent_mom_delta": spent_mom_delta,
        "net_mom_delta": net_mom_delta,
        "income_mom_pct": income_mom_pct,
        "spent_mom_pct": spent_mom_pct,
        "net_mom_pct": net_mom_pct,
        # best/worst
        "best_net_month_value": float(best_net),
        "best_net_month_label": best_label,
        "worst_net_month_value": float(worst_net),
        "worst_net_month_label": worst_label,
    }

    cashflow = {
        "labels": labels,
        "income": income_results,
        "spent": spent_results,
        "net": net_results,
    }

    return {
        "widgets": widgets,
        "cashflow": cashflow,
        "recents": {},
    }
