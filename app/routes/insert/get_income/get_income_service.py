import calendar

MONTHS = list(calendar.month_name)[1:]  # ["January", ..., "December"]

def blank_year_dict():
    return {m: 0.0 for m in MONTHS}

def run(connector):
    rows = connector.run_query("""
        SELECT person_nm, month, year, income
        FROM financial.income
    """)

    output = {}
    for person_nm, month_name, year, income in rows:
        year = int(year)

        if person_nm not in output:
            output[person_nm] = {}
        if year not in output[person_nm]:
            output[person_nm][year] = blank_year_dict()

        # only set known months
        if month_name in output[person_nm][year]:
            output[person_nm][year][month_name] = float(income or 0)

    return output
