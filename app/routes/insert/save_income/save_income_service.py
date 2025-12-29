import calendar

MONTHS = list(calendar.month_name)[1:]  # ["January", ..., "December"]
MONTH_SET = set(MONTHS)
MONTH_BY_INT = {i: MONTHS[i] for i in range(12)}  # 0->January ... 11->December

def normalize_month_key(k):
    """
    Accepts:
      - "January" / " january " / "JANUARY"
      - 0..11 (int) or "0".."11" (str)
    Returns canonical month name ("January"...).
    """
    # int index
    if isinstance(k, int):
        if 0 <= k <= 11:
            return MONTH_BY_INT[k]
        return None

    # string: maybe digit, maybe month name
    if isinstance(k, str):
        s = k.strip()
        if s.isdigit():
            i = int(s)
            if 0 <= i <= 11:
                return MONTH_BY_INT[i]
            return None

        # normalize case: "january" -> "January"
        s = s[:1].upper() + s[1:].lower() if s else s
        return s if s in MONTH_SET else None

    return None


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
    except (ValueError, TypeError):
        return {"error": "Invalid year"}, 400

    # Build month -> amount (float)
    month_amounts = {}
    for k, v in income_view.items():
        month_name = normalize_month_key(k)
        if not month_name:
            continue
        try:
            amt = float(v)
        except (ValueError, TypeError):
            amt = 0.0
        month_amounts[month_name] = amt

    sql = """
        INSERT INTO financial.income (person_nm, month, year, income)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (person_nm, year, month)
        DO UPDATE SET income = EXCLUDED.income, updated_at = now()
    """

    # Always write all 12 months (default 0 if missing)
    rows = [(person, m, year, month_amounts.get(m, 0.0)) for m in MONTHS]

    with connector.connect() as conn:
        with conn.cursor() as cur:
            # Ensure person exists (FK safety)
            cur.execute("SELECT 1 FROM financial.ppl_info WHERE person_nm = %s", (person,))
            if not cur.fetchone():
                return {"error": f"Unknown user '{person}'"}, 400

            cur.executemany(sql, rows)

    return {"ok": True, "user": person, "year": year}, 200
