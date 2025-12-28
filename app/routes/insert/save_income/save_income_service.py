import calendar

MONTHS = list(calendar.month_name)[1:]  # ["January", ..., "December"]

def save_income(connector, data):
    person = (data.get("user") or "").strip()
    year = data.get("year")
    income_view = data.get("income") or {}

    if not person:
        return {"error": "Missing user"}, 400
    if year is None:
        return {"error": "Missing year"}, 400

    try:
        year = int(year)
    except ValueError:
        return {"error": "Invalid year"}, 400

    # Convert income_view keys (0..11) to ints, values to floats
    month_amounts = {}
    for k, v in income_view.items():
        try:
            idx = int(k)  # keys might arrive as strings "0".."11"
        except (ValueError, TypeError):
            continue
        if idx < 0 or idx > 11:
            continue
        try:
            amt = float(v)
        except (ValueError, TypeError):
            amt = 0.0
        month_amounts[idx] = amt

    # Upsert statement (person_nm, year, month is PK)
    sql = """
        INSERT INTO financial.income (person_nm, month, year, income)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (person_nm, year, month)
        DO UPDATE SET income = EXCLUDED.income, updated_at = now()
    """

    # Batch rows for 12 months (default 0 if missing)
    rows = []
    for idx in range(12):
        month_name = MONTHS[idx]
        amt = month_amounts.get(idx, 0.0)
        rows.append((person, month_name, year, amt))

    with connector.connect() as conn:
        with conn.cursor() as cur:
            # (Optional) ensure person exists in ppl_info to satisfy FK
            cur.execute("SELECT 1 FROM financial.ppl_info WHERE person_nm = %s", (person,))
            if not cur.fetchone():
                return {"error": f"Unknown user '{person}'"}, 400

            cur.executemany(sql, rows)

    return {"ok": True, "user": person, "year": year}, 200
