def run(connector):
    rows = connector.run_query(
        """
        SELECT person_nm, month, year, income
        FROM financial.income
    """
    )

    output = {}
    for row in rows:
        person_nm = row[0]
        month_name = row[1] # "January", ..., "December"
        year = row[2]
        income = row[3]
        if person_nm not in output:
            output[person_nm] = {}
        if year not in output[person_nm]:
            output[person_nm][year] = [0.0] * 12
        output[person_nm][year][month_name] = float(income)

    return output
