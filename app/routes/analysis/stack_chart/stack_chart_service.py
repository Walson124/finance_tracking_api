import os
from app.utils.query_parser import parse_query

def get_data(connector):
    try:
        query = parse_query(
            os.path.join(os.path.dirname(__file__), 'sql', 'get_data.sql'),
        )
        result = connector.run_query(query)
        result = [{'year': r[0], 'month': r[1], 'category': r[2], 'sum': r[3]} for r in result]

        # for stack by category we want category: [sum_year_mo1, sum_year_mo2, ...]
        # if year_mo doesn't exist for given category, sum_year_mo should be 0
        distinct_ym = sorted({(r["year"], r["month"]) for r in result})
        stacked = {r["category"]: [0] * len(distinct_ym) for r in result}
        for r in result:
            idx = distinct_ym.index((r["year"], r["month"]))
            stacked[r["category"]][idx] = r["sum"]
        if "" in stacked:
            stacked['unassigned'] = stacked.pop("")
        return stacked
    except Exception as e:
        print(e)
    return []