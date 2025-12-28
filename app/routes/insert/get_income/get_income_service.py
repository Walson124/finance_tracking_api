def run(connector):
    rows = connector.run_query(
        """
        SELECT person_nm, month, year, income
        FROM financial.income
    """
    )

    output = {}
    for row in rows:
        if row["person_nm"] not in output:
            output[row["person_nm"]] = {}
        if row["year"] not in output[row["person_nm"]]:
            output[row["person_nm"]][row["year"]] = [0.0] * 12
        output[row["person_nm"]][row["year"]][row["month"] - 1] = float(row["income"])

    return output
